import joblib
import numpy as np

model = joblib.load("app/ml/fraud_model.pkl")

def ml_score(transaction):
    data = np.array([[transaction.amount, transaction.lat, transaction.lon, transaction.hour]])
    score = model.decision_function(data)
    return float(score[0])
