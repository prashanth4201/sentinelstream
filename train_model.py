from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
import os

# create folder if not exists
os.makedirs("models", exist_ok=True)

# dummy training data
X = np.array([
    [200, 1],
    [500, 1],
    [1000, 1],
    [7000, 0],
    [9000, 0]
])

# train model
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X)

# SAVE MODEL ✅
joblib.dump(model, "models/fraud_iforest.pkl")

print("Model saved successfully!")
