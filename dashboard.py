import streamlit as st
import psutil
import joblib
import numpy as np
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Incident Predictor Dashboard", layout="wide")
refresh_interval = st.sidebar.slider("Refresh every (seconds)", 2, 10, 5)
st_autorefresh(interval=refresh_interval * 1000, limit=None, key="dashboard_refresh")

@st.cache_resource
def load_model():
    return joblib.load("incident_predictor_model1.pkl")

model = load_model()

cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory().percent

st.title("Incident Predictor")
st.markdown("Shows only anomalous processes detected via log-based metrics.")

st.subheader("System Overview")
col1, col2 = st.columns(2)
col1.metric("CPU Usage (%)", f"{cpu:.1f}")
col2.metric("Memory Usage (%)", f"{mem:.1f}")

processes = []
for proc in psutil.process_iter(attrs=["pid", "name"]):
    try:
        proc.cpu_percent(interval=None)
    except:
        continue
import time
time.sleep(1)

for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
    try:
        if proc.info["cpu_percent"] >= 1.0:
            processes.append(proc.info)
    except:
        continue

anomalies = []
for proc in processes:
    name = proc["name"]
    pid = proc["pid"]
    pcpu = proc["cpu_percent"]
    pmem = proc["memory_percent"]
    x = np.array([[cpu, mem, pcpu, pmem]])
    try:
        pred = model.predict(x)[0]
        if pred == -1:
            anomalies.append({
                "Process": name,
                "PID": pid,
                "CPU %": pcpu,
                "Mem %": pmem,
                "System CPU": cpu,
                "System Mem": mem
            })
    except:
        continue

st.subheader("Anomalous Processes")
if anomalies:
    df = pd.DataFrame(anomalies)
    st.dataframe(df, use_container_width=True)
else:
    st.success("No anomalies detected.")
