import pandas as pd
import os

INPUT_FILE = "metrics1.csv"
OUTPUT_FILE = "labeled_metrics1.csv"

try:
    df = pd.read_csv(INPUT_FILE)

    df["status"] = "Normal"

    df.loc[df["cpu_usage"] > 90, "status"] = "High CPU Load"
    df.loc[df["memory_usage"] > 85, "status"] = "High Memory Usage"
    df.loc[df["process_cpu"] > 50, "status"] = "High Process Usage"

    df.to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE), index=False)

    print(f"Dataset labeled and appended to {OUTPUT_FILE}")

except Exception as e:
    print(f"Error processing dataset: {e}")
