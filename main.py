import argparse,csv,time
from pathlib import Path
import cv2,numpy as np,yaml
from ultralytics import YOLO
from roadsense.analytics import Event,collision_risk_pairs,congestion_state,update_track_analytics,wrong_way
from roadsense.tracker_state import TrackStore
from roadsense.visualization import draw_alert,draw_header,draw_track

def load_cfg(p):
    with open(p,encoding='utf-8') as f:return yaml.safe_load(f)
def ensure_csv(p,headers):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():
        with p.open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerow(headers)
def log_event(p,e):
    ensure_csv(p,['timestamp','event_type','track_id','severity','message'])
    with open(p,'a',newline='',encoding='utf-8') as f:csv.writer(f).writerow([time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(e.timestamp)),e.event_type,e.track_id or '',e.severity,e.message])
def log_metric(p,t,count,avg,congestion):
    ensure_csv(p,['timestamp','vehicle_count','avg_speed_kmh','congestion'])
    with open(p,'a',newline='',encoding='utf-8') as f:csv.writer(f).writerow([time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t)),count,round(avg,2),congestion])
def source(s): return int(s) if s.isdigit() else s

def main(args):
    cfg=load_cfg(args.config); mc=cfg['model']; model=YOLO(args.model or mc['checkpoint'])
    cap=cv2.VideoCapture(source(args.source))
    if not cap.isOpened(): raise RuntimeError(f'Could not open source: {args.source}')
    store=TrackStore(); event_csv=cfg['logging']['events_csv']; metric_csv=cfg['logging']['metrics_csv']; seen=set(); last_metric=0; start=time.time(); frames=0
    while True:
        ok,frame=cap.read()
        if not ok: break
        now=time.time();frames+=1;fps=frames/max(now-start,1e-6)
        results=model.track(frame,persist=True,tracker=mc['tracker'],conf=mc['confidence'],iou=mc['iou'],imgsz=mc['imgsz'],classes=cfg['classes'],verbose=False)
        r=results[0]; tracks=[]
        if r.boxes is not None and len(r.boxes):
            boxes=r.boxes.xyxy.cpu().numpy(); classes=r.boxes.cls.cpu().numpy().astype(int)
            ids=r.boxes.id.cpu().numpy().astype(int) if r.boxes.id is not None else np.arange(len(boxes))+1000000
            for box,cls_id,tid in zip(boxes,classes,ids):
                tid=int(tid); x1,y1,x2,y2=box; track=store.get_or_create(tid,model.names[int(cls_id)])
                track.add_point((x1+x2)/2,(y1+y2)/2,now); stopped=update_track_analytics(track,now,cfg['speed']['pixels_per_meter'],cfg['stopped_vehicle']['min_speed_kmh']); tracks.append(track); draw_track(frame,box,track)
                if cfg['stopped_vehicle']['enabled'] and stopped>=cfg['stopped_vehicle']['seconds'] and ('stop',tid) not in seen:
                    seen.add(('stop',tid));log_event(event_csv,Event(now,'STOPPED_VEHICLE',tid,'MEDIUM',f'{track.cls_name} ID {tid} stopped for {stopped:.1f}s'))
                if cfg['direction']['enabled'] and wrong_way(track,cfg['direction']['expected_vector'],cfg['direction']['tolerance_degrees'],cfg['direction']['min_displacement_px']) and ('wrong',tid) not in seen:
                    seen.add(('wrong',tid));log_event(event_csv,Event(now,'WRONG_WAY',tid,'HIGH',f'{track.cls_name} ID {tid} appears to move against expected direction'))
        store.cleanup(now); congestion=congestion_state(tracks,cfg['congestion']['high_vehicle_count'],cfg['congestion']['medium_vehicle_count'],cfg['congestion']['low_average_speed_kmh']);avg=float(np.mean([t.last_speed_kmh for t in tracks])) if tracks else 0.0;alerts=[]
        for a,b,ttc,dist in collision_risk_pairs(tracks,cfg['collision']['max_pair_distance_px'],cfg['collision']['min_closing_speed_px_s'],cfg['collision']['critical_ttc_seconds']):
            key=('collision',min(a,b),max(a,b))
            if key not in seen: seen.add(key);log_event(event_csv,Event(now,'COLLISION_RISK',None,'HIGH',f'IDs {a} and {b}: estimated TTC {ttc:.2f}s at {dist:.0f}px'))
            alerts.append(f'COLLISION RISK: ID {a} <-> ID {b} | TTC {ttc:.2f}s')
        if congestion=='HIGH':alerts.append('HIGH CONGESTION')
        draw_header(frame,len(tracks),congestion,fps,len(seen))
        for i,a in enumerate(alerts[:3]):draw_alert(frame,a,82+i*42)
        cv2.putText(frame,'Press Q to quit',(18,frame.shape[0]-18),cv2.FONT_HERSHEY_SIMPLEX,.5,(220,220,220),1)
        if now-last_metric>=1:log_metric(metric_csv,now,len(tracks),avg,congestion);last_metric=now
        cv2.imshow('RoadSense AI',frame)
        if cv2.waitKey(1)&0xFF==ord('q'):break
    cap.release();cv2.destroyAllWindows()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='0');p.add_argument('--model');p.add_argument('--config',default='config.yaml');main(p.parse_args())
