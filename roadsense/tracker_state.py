from collections import deque
from dataclasses import dataclass, field
import time

@dataclass
class TrackState:
    track_id: int
    cls_name: str
    points: deque = field(default_factory=lambda: deque(maxlen=40))
    last_seen: float = field(default_factory=time.time)
    stopped_since: float | None = None
    last_speed_kmh: float = 0.0
    last_direction_deg: float = 0.0

    def add_point(self, x, y, timestamp):
        self.points.append((float(x), float(y), float(timestamp)))
        self.last_seen = timestamp

    def velocity_px_s(self):
        if len(self.points) < 2: return 0.0, 0.0
        x1,y1,t1 = self.points[-2]; x2,y2,t2 = self.points[-1]
        dt=max(t2-t1,1e-6)
        return (x2-x1)/dt,(y2-y1)/dt

    def recent_displacement(self, n=5):
        if len(self.points)<2: return 0.0,0.0
        p=list(self.points)[-max(2,n):]
        return p[-1][0]-p[0][0],p[-1][1]-p[0][1]

class TrackStore:
    def __init__(self,max_age_seconds=2.0):
        self.tracks={}; self.max_age_seconds=max_age_seconds
    def get_or_create(self,track_id,cls_name):
        if track_id not in self.tracks: self.tracks[track_id]=TrackState(track_id,cls_name)
        else: self.tracks[track_id].cls_name=cls_name
        return self.tracks[track_id]
    def cleanup(self,now):
        for tid in [k for k,v in self.tracks.items() if now-v.last_seen>self.max_age_seconds]: del self.tracks[tid]
