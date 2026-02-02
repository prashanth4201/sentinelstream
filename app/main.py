from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import time
import redis

from app.ml.scoring import ml_score
from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.rules.rule_engine import RuleEngine
from app.routes.fraud_rules import router as fraud_rules_router

app = FastAPI(title="SentinelStream")

# Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

rule_engine = RuleEngine()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "SentinelStream running"}

# 🔥 TRANSACTION ENDPOINT (ML + RULES + LATENCY)
@app.post("/transaction")
def create_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db)
):
    start = time.time()  # ⏱ start latency timer

    ml_risk = ml_score(txn)
    rules_triggered = rule_engine.evaluate(txn)

    final_risk = "LOW"
    if ml_risk < -0.3 or "HIGH_AMOUNT" in rules_triggered:
        final_risk = "HIGH"

    record = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        risk=final_risk
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    latency = time.time() - start  # ⏱ end latency timer
    print("Transaction latency:", latency)

    return {
        "risk": final_risk,
        "ml_score": ml_risk,
        "rules_triggered": rules_triggered,
        "latency": latency
    }

# 🔍 ALL TRANSACTION HISTORY (ONE CLICK)
@app.get("/transactions", response_model=List[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

# Fraud rules
app.include_router(fraud_rules_router)
