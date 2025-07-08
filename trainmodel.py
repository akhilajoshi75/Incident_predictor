import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
FILE_PATH = "labeled_metrics1.csv"
print(" Loading data...")
df = pd.read_csv(FILE_PATH, dtype={"pid": str})
print("Data loaded successfully!")
features = ["cpu_usage", "memory_usage", "process_cpu", "process_memory"]
X = df[features].values
print("Training Isolation Forest model...")
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)
print("Model training complete!")
joblib.dump(model, "incident_predictor_model1.pkl")
print(f"Model saved as 'incident_predictor_model.pkl1' with {X.shape[1]} features.")
