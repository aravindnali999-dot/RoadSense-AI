from dataclasses import dataclass
from itertools import combinations
import math
import numpy as np

@dataclass
class Event:
    timestamp: float
    event_type: str
    track_id: int|None
    severity: str
    message: str

def speed_from_track(track,pixels_per_meter):
    vx,vy=track.velocity_px_s(); return math.hypot(vx,vy)/max(pixels_per_meter,1e-6)*3.6

def direction_degrees(track):
    vx,vy=track.velocity_px_s()
    return math.degrees(math.atan2(vy,vx)) if math.hypot(vx,vy)>1e-6 else 0.0

def angle_difference_deg(a,b): return abs((a-b+180)%360-180)

def update_track_analytics(track,now,pixels_per_meter,min_speed_kmh):
    track.last_speed_kmh=speed_from_track(track,pixels_per_meter); track.last_direction_deg=direction_degrees(track)
    if track.last_speed_kmh<=min_speed_kmh:
        if track.stopped_since is None: track.stopped_since=now
    else: track.stopped_since=None
    return 0.0 if track.stopped_since is None else now-track.stopped_since

def congestion_state(tracks,high_count,medium_count,low_average_speed):
    tracks=list(tracks); count=len(tracks); avg=float(np.mean([t.last_speed_kmh for t in tracks])) if tracks else 0.0
    if count>=high_count or (count>=medium_count and avg<=low_average_speed): return 'HIGH'
    if count>=medium_count: return 'MEDIUM'
    return 'LOW'

def wrong_way(track,expected_vector,tolerance_degrees,min_displacement_px):
    dx,dy=track.recent_displacement(); mag=math.hypot(dx,dy)
    ex,ey=expected_vector; emag=math.hypot(ex,ey)
    if mag<min_displacement_px or emag<1e-6: return False
    dot=max(-1,min(1,(dx*ex+dy*ey)/(mag*emag)))
    return math.degrees(math.acos(dot))>tolerance_degrees

def collision_risk_pairs(tracks,max_distance_px,min_closing_speed_px_s,critical_ttc_s):
    out=[]
    for a,b in combinations(list(tracks),2):
        if len(a.points)<2 or len(b.points)<2: continue
        ax,ay,_=a.points[-1]; bx,by,_=b.points[-1]
        rel=np.array([bx-ax,by-ay],float); dist=float(np.linalg.norm(rel))
        if dist<1 or dist>max_distance_px: continue
        av=np.array(a.velocity_px_s()); bv=np.array(b.velocity_px_s()); rv=bv-av
        closing=float(-np.dot(rv,rel/dist))
        if closing<min_closing_speed_px_s: continue
        ttc=dist/max(closing,1e-6)
        if ttc<=critical_ttc_s: out.append((a.track_id,b.track_id,ttc,dist))
    return out
