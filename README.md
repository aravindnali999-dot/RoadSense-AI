# RoadSense AI — Real-Time Traffic Intelligence & Incident Detection

A runnable computer-vision portfolio project using YOLO + multi-object tracking + trajectory analytics. It detects vehicles, keeps persistent IDs, estimates approximate speed, scores congestion, flags stopped vehicles and wrong-way motion, and uses a simple time-to-collision heuristic for close moving pairs. Events and metrics are written to CSV, with an optional Streamlit dashboard.

## Run

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python main.py --source 0
```

Video file:
```bash
python main.py --source path/to/traffic.mp4
```

Dashboard:
```bash
streamlit run dashboard.py
```

## Calibration

`config.yaml` contains `pixels_per_meter`. Replace 40.0 with a value calibrated for your camera. Monocular speed is only an estimate without proper camera calibration/homography. Collision-risk is also a heuristic, not a safety-certified predictor.

## LinkedIn demo

Record 30–60 seconds showing live IDs, trajectories, congestion changes, and an incident alert. Then show `outputs/events.csv` and the Streamlit dashboard.

Suggested title: **RoadSense AI — Real-Time Traffic Intelligence & Incident Detection**

Suggested one-liner: *Built a real-time computer-vision system that detects, tracks, and analyzes road traffic using YOLO, multi-object tracking, trajectory analytics, and event detection.*
