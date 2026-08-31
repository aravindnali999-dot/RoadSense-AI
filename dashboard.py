from pathlib import Path
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="RoadSense AI",
    page_icon="🚦",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #8b949e;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 25px;
    }

    .status-box {
        padding: 12px 18px;
        border-radius: 10px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------
metrics_file = Path("outputs/metrics.csv")
events_file = Path("outputs/events.csv")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">🚦 RoadSense AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Real-time traffic intelligence, vehicle tracking and road safety analytics'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# CHECK DATA
# ---------------------------------------------------------
if not metrics_file.exists():
    st.error("Traffic metrics were not found.")
    st.info(
        "Run the detection pipeline first:\n\n"
        "`python main.py --source data\\traffic.mp4`"
    )
    st.stop()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
metrics = pd.read_csv(metrics_file)

if events_file.exists():
    events = pd.read_csv(events_file)
else:
    events = pd.DataFrame(
        columns=[
            "timestamp",
            "event_type",
            "track_id",
            "severity",
            "message"
        ]
    )

# ---------------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------------
if not metrics.empty:
    metrics["timestamp"] = pd.to_datetime(metrics["timestamp"])

if not events.empty:
    events["timestamp"] = pd.to_datetime(events["timestamp"])

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Dashboard Controls")

    st.write("RoadSense AI monitoring configuration")

    if not metrics.empty:
        latest_time = metrics["timestamp"].max()

        st.markdown("### Latest Analysis")
        st.write(latest_time.strftime("%Y-%m-%d %H:%M:%S"))

    st.markdown("### Detection Modules")

    st.checkbox("Vehicle Detection", value=True, disabled=True)
    st.checkbox("Vehicle Tracking", value=True, disabled=True)
    st.checkbox("Speed Estimation", value=True, disabled=True)
    st.checkbox("Congestion Detection", value=True, disabled=True)
    st.checkbox("Wrong-Way Detection", value=True, disabled=True)
    st.checkbox("Collision Risk", value=True, disabled=True)

    st.divider()

    st.caption("RoadSense AI")
    st.caption("Computer Vision + Traffic Analytics")

# ---------------------------------------------------------
# CURRENT METRICS
# ---------------------------------------------------------
latest = metrics.iloc[-1]

latest_vehicle_count = int(latest["vehicle_count"])
latest_speed = float(latest["avg_speed_kmh"])
latest_congestion = str(latest["congestion"])

incident_count = len(events)

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Live Traffic Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🚗 Vehicles Detected",
    latest_vehicle_count
)

c2.metric(
    "🏎️ Average Speed",
    f"{latest_speed:.1f} km/h"
)

c3.metric(
    "🚦 Congestion Level",
    latest_congestion
)

c4.metric(
    "⚠️ Safety Incidents",
    incident_count
)

# ---------------------------------------------------------
# ADDITIONAL STATISTICS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Traffic Statistics</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4)

average_vehicle_count = metrics["vehicle_count"].mean()
maximum_vehicle_count = metrics["vehicle_count"].max()
maximum_speed = metrics["avg_speed_kmh"].max()
average_speed = metrics["avg_speed_kmh"].mean()

s1.metric(
    "Average Vehicles",
    f"{average_vehicle_count:.1f}"
)

s2.metric(
    "Peak Vehicles",
    int(maximum_vehicle_count)
)

s3.metric(
    "Peak Estimated Speed",
    f"{maximum_speed:.1f} km/h"
)

s4.metric(
    "Overall Avg Speed",
    f"{average_speed:.1f} km/h"
)

# ---------------------------------------------------------
# TRAFFIC VOLUME
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🚗 Traffic Volume Over Time</div>',
    unsafe_allow_html=True
)

chart_metrics = metrics.copy()

chart_metrics["timestamp"] = pd.to_datetime(
    chart_metrics["timestamp"],
    errors="coerce"
)

chart_metrics = (
    chart_metrics
    .dropna(subset=["timestamp"])
    .sort_values("timestamp")
    .tail(60)
)

# Use a regular numeric index for the chart.
# This prevents Streamlit from drawing a misleading line
# across large gaps in timestamps.
traffic_chart = chart_metrics[
    ["timestamp", "vehicle_count"]
].copy()

traffic_chart["Time"] = traffic_chart["timestamp"].dt.strftime(
    "%H:%M:%S"
)

traffic_chart = traffic_chart.set_index("Time")

st.line_chart(
    traffic_chart[["vehicle_count"]],
    height=350
)


# ---------------------------------------------------------
# SPEED
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🏎️ Estimated Vehicle Speed</div>',
    unsafe_allow_html=True
)

speed_chart = chart_metrics[
    ["timestamp", "avg_speed_kmh"]
].copy()

speed_chart["Time"] = speed_chart["timestamp"].dt.strftime(
    "%H:%M:%S"
)

speed_chart = speed_chart.set_index("Time")

st.line_chart(
    speed_chart[["avg_speed_kmh"]],
    height=350
)
# ---------------------------------------------------------
# INCIDENT ANALYTICS
# ---------------------------------------------------------
if not events.empty:

    st.markdown(
        '<div class="section-title">⚠️ Safety Incident Analytics</div>',
        unsafe_allow_html=True
    )

    # Incident counts
    incident_counts = (
        events["event_type"]
        .value_counts()
        .rename_axis("Incident Type")
        .reset_index(name="Count")
    )

    a1, a2 = st.columns(2)

    with a1:
        st.subheader("Incident Types")
        st.bar_chart(
            incident_counts.set_index("Incident Type")
        )

    with a2:
        st.subheader("Severity Distribution")

        severity_counts = (
            events["severity"]
            .value_counts()
            .rename_axis("Severity")
            .reset_index(name="Count")
        )

        st.bar_chart(
            severity_counts.set_index("Severity")
        )

    # -----------------------------------------------------
    # INCIDENT SUMMARY
    # -----------------------------------------------------
    st.subheader("🚨 Incident Summary")

    wrong_way_count = len(
        events[events["event_type"] == "WRONG_WAY"]
    )

    stopped_count = len(
        events[events["event_type"] == "STOPPED_VEHICLE"]
    )

    collision_count = len(
        events[events["event_type"] == "COLLISION_RISK"]
    )

    i1, i2, i3 = st.columns(3)

    i1.metric(
        "🔄 Wrong-Way Events",
        wrong_way_count
    )

    i2.metric(
        "🛑 Stopped Vehicles",
        stopped_count
    )

    i3.metric(
        "💥 Collision Risks",
        collision_count
    )

    # -----------------------------------------------------
    # INCIDENT LOG
    # -----------------------------------------------------
    st.subheader("📋 Recent Incident Log")

    display_events = events.tail(100).copy()

    st.dataframe(
        display_events,
        width="stretch",
        hide_index=True
    )

else:

    st.success("✅ No traffic safety incidents recorded.")

# ---------------------------------------------------------
# SYSTEM STATUS
# ---------------------------------------------------------
st.divider()

st.markdown(
    '<div class="section-title">🟢 System Status</div>',
    unsafe_allow_html=True
)

status1, status2, status3 = st.columns(3)

with status1:
    st.success("Vehicle Detection: ACTIVE")

with status2:
    st.success("Traffic Analytics: ACTIVE")

with status3:
    st.success("Event Logging: ACTIVE")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "RoadSense AI | Computer Vision Traffic Intelligence System"
)