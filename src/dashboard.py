import sqlite3
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

DB_PATH = Path("data/pipeline.db")

st.set_page_config(page_title="Anomaly Pipeline", layout="wide")
st.title("Cloud Anomaly Detection Pipeline")

if not DB_PATH.exists():
    st.warning("No data yet. Start the worker and the simulator first.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM results ORDER BY id", conn)
conn.close()

if df.empty:
    st.warning("The database is empty. Start the worker and the simulator.")
    st.stop()

df["ts"] = pd.to_datetime(df["ts"])

st.sidebar.header("Controls")
metric = st.sidebar.selectbox("Metric", sorted(df["metric"].unique()))
last_n = st.sidebar.slider("Readings to show", 200, 5000, 1000, step=100)
auto = st.sidebar.checkbox("Auto refresh (every 2 seconds)", value=False)

m = df[df["metric"] == metric]
flags = m[m["is_anomaly"] == 1].sort_values("ts")

if len(flags):
    incidents = int((flags["ts"].diff() > pd.Timedelta(minutes=60)).sum()) + 1
else:
    incidents = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Readings processed", f"{len(m):,}")
c2.metric("Anomalies flagged", f"{len(flags):,}")
c3.metric("Incidents (grouped)", incidents)
c4.metric("Flag rate", f"{len(flags) / len(m) * 100:.2f}%")

view = m.tail(last_n)
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(view["ts"], view["value"], linewidth=0.8, label="value")

colors = {"LOW": "orange", "MEDIUM": "red", "HIGH": "darkred"}
for sev, color in colors.items():
    pts = view[(view["is_anomaly"] == 1) & (view["severity"] == sev)]
    if len(pts):
        ax.scatter(pts["ts"], pts["value"], color=color, s=25, zorder=3, label=sev)

ax.set_title(metric)
ax.legend(loc="upper left")
fig.autofmt_xdate()
st.pyplot(fig)
plt.close(fig)

st.subheader("Latest alerts")
latest = flags.sort_values("ts", ascending=False).head(20)
st.dataframe(latest[["ts", "value", "zscore", "severity"]], use_container_width=True)

st.caption("Severity shows how far a reading is from its recent normal. "
           "On the tested data it did not predict which alerts match labeled anomalies.")

if auto:
    time.sleep(2)
    st.rerun()