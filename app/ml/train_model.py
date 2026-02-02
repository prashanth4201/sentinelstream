import joblib
import os
import numpy as np
from sklearn.ensemble import IsolationForest

# Fake training data (transaction amounts)
X = np.array([
    [100], [200], [500], [1000],
    [3000], [7000], [12000], [20000]
])

model = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

model.fit(X)

# Save model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")
joblib.dump(model, MODEL_PATH)

print("✅ Isolation Forest model saved at:", MODEL_PATH)
