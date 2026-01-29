import joblib
import numpy as np

model = joblib.load("app/ml/fraud_model.pkl")

def ml_score(txn):
    data = np.array([[txn.amount, 0, 0, 0]])
    return float(model.decision_function(data)[0])
