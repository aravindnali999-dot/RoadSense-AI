# 🚦 RoadSense AI — Real-Time Traffic Intelligence & Incident Detection

RoadSense AI is an end-to-end computer-vision system for analyzing road traffic from video streams.

The system combines **YOLO-based object detection, multi-object tracking, trajectory analysis, traffic metrics, and event detection** to provide real-time traffic intelligence.

## ✨ Features

- 🚗 Vehicle detection using YOLO
- 🆔 Persistent vehicle IDs through multi-object tracking
- 📈 Approximate vehicle-speed estimation
- 🚦 Traffic congestion scoring
- 🛑 Stopped-vehicle detection
- ↔️ Wrong-way movement detection
- ⚠️ Collision-risk detection using a time-to-collision (TTC) heuristic
- 📊 Timestamped traffic metrics
- 📝 Incident/event logging to CSV
- 📺 Real-time annotated video output
- 📊 Interactive Streamlit analytics dashboard

## 🏗️ System Architecture

```text
Traffic Video / Camera
        ↓
YOLO Object Detection
        ↓
Multi-Object Tracking
        ↓
Persistent Vehicle IDs
        ↓
Trajectory Analysis
        ↓
┌──────────────────────────────┐
│ Speed Estimation             │
│ Congestion Analysis          │
│ Stopped Vehicle Detection    │
│ Wrong-Way Detection          │
│ Collision-Risk Analysis      │
└──────────────────────────────┘
        ↓
CSV Metrics + Incident Logs
        ↓
Streamlit Dashboard
