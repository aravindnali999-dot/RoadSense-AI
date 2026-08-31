# 🚦 RoadSense AI — Real-Time Traffic Intelligence & Incident Detection

> An AI-powered computer vision system for real-time vehicle detection, tracking, speed estimation, congestion analysis, and road-safety event detection.

RoadSense AI analyzes traffic video using **YOLO-based object detection, multi-object tracking, trajectory analysis, and event detection**. The system assigns persistent vehicle IDs, estimates approximate vehicle speeds, evaluates congestion, detects stopped and wrong-way vehicles, and identifies potential collision-risk situations.

A **Streamlit dashboard** provides real-time traffic analytics and visualizes vehicle counts, estimated speed, congestion levels, and safety incidents.

---

## 🎯 Project Overview

RoadSense AI is designed as an end-to-end traffic intelligence pipeline:

```text
Traffic Video / Camera
        │
        ▼
┌──────────────────────┐
│ Vehicle Detection    │
│ YOLO-based Model     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Multi-Object         │
│ Tracking              │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Trajectory Analysis  │
└──────────┬───────────┘
           │
     ┌─────┼──────────────┐
     ▼     ▼              ▼
   Speed  Congestion   Incident
 Estimation Analysis   Detection
     │     │              │
     └─────┼──────────────┘
           ▼
     CSV Metrics & Events
           │
           ▼
    Streamlit Dashboard
