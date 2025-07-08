import time
import psutil
import joblib
import numpy as np
import logging
try:
    model = joblib.load("incident_predictor_model1.pkl")
    print("Model loaded successfully.\n")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_system_metrics():
    return psutil.cpu_percent(interval=1), psutil.virtual_memory().percent

def get_active_processes(threshold=1.0):
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            proc.cpu_percent(interval=None) 
        except:
            continue
    time.sleep(1)
    processes = []
    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            if proc.info["cpu_percent"] >= threshold:
                processes.append(proc.info)
        except:
            continue
    return processes

def monitor():
    print("Monitoring for anomalies...\n")
    while True:
        cpu, mem = get_system_metrics()
        processes = get_active_processes()

        for proc in processes:
            name = proc['name']
            pid = proc['pid']
            pcpu = proc['cpu_percent']
            pmem = proc['memory_percent']

            input_features = np.array([[cpu, mem, pcpu, pmem]])
            try:
                pred = model.predict(input_features)[0]
                if pred == -1:
                    print(f"Anomaly Detected!")
                    print(f"   Process: {name} (PID {pid})")
                    print(f"   CPU: {pcpu:.1f}%, Mem: {pmem:.1f}%, System CPU: {cpu:.1f}%, System Mem: {mem:.1f}%")
                    print("-" * 50)
            except Exception as e:
                logging.warning(f"Prediction failed for {name}: {e}")
        time.sleep(5)
if __name__ == "__main__":
    monitor()
