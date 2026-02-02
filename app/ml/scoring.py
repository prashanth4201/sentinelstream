import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "isolation_forest.pkl")

model = joblib.load(MODEL_PATH)

def ml_score(txn):
    features = [[txn.amount]]
    return model.decision_function(features)[0]
