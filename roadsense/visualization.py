import cv2

def draw_track(frame,box,track,color=(0,220,255)):
    x1,y1,x2,y2=map(int,box); cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
    label=f'ID {track.track_id} | {track.cls_name} | {track.last_speed_kmh:.1f} km/h'
    cv2.rectangle(frame,(x1,max(0,y1-25)),(min(frame.shape[1]-1,x1+300),y1),color,-1)
    cv2.putText(frame,label,(x1+5,y1-7),cv2.FONT_HERSHEY_SIMPLEX,.48,(0,0,0),1,cv2.LINE_AA)
    pts=list(track.points)
    for a,b in zip(pts[:-1],pts[1:]): cv2.line(frame,(int(a[0]),int(a[1])),(int(b[0]),int(b[1])),color,2)

def draw_header(frame,count,congestion,fps,incidents):
    cv2.rectangle(frame,(0,0),(frame.shape[1],70),(12,18,28),-1)
    cv2.putText(frame,'ROADSENSE AI',(18,28),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2)
    cv2.putText(frame,f'Vehicles: {count}',(18,56),cv2.FONT_HERSHEY_SIMPLEX,.5,(180,220,255),1)
    cv2.putText(frame,f'Congestion: {congestion}',(170,56),cv2.FONT_HERSHEY_SIMPLEX,.5,(180,220,255),1)
    cv2.putText(frame,f'FPS: {fps:.1f}',(355,56),cv2.FONT_HERSHEY_SIMPLEX,.5,(180,220,255),1)
    cv2.putText(frame,f'Incidents: {incidents}',(450,56),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,210,130),1)

def draw_alert(frame,text,y=82):
    cv2.rectangle(frame,(12,y),(min(frame.shape[1]-12,700),y+34),(30,35,45),-1)
    cv2.rectangle(frame,(12,y),(18,y+34),(0,80,255),-1)
    cv2.putText(frame,text,(28,y+23),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1,cv2.LINE_AA)
