from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

X = np.random.rand(1000, 4)

model = IsolationForest(contamination=0.05)
model.fit(X)

joblib.dump(model, BASE_DIR / "fraud_model.pkl")

print("fraud_model.pkl created")
