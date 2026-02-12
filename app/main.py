from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import time
import redis

from app.ml.scoring import ml_score
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.rules.rule_engine import RuleEngine
from app.routes.fraud_rules import router as fraud_rules_router

app = FastAPI(title="SentinelStream")

# ✅ CREATE TABLES AUTOMATICALLY
Base.metadata.create_all(bind=engine)

# 🔹 Redis (Safe Initialization - will NOT crash if not running)
try:
    redis_client = redis.Redis(
        host="redis", # works inside Docker
        port=6379,
        decode_responses=True
    )
    redis_client.ping()
except:
    redis_client = None

rule_engine = RuleEngine()


# 🔹 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "SentinelStream running"}


# 🔥 TRANSACTION ENDPOINT
@app.post("/transaction")
def create_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db)
):
    start = time.time()

    cache_hit = False
    if redis_client:
        try:
            cache_key = f"user:{txn.user_id}"
            cached = redis_client.get(cache_key)
            if cached:
                cache_hit = True
            else:
                redis_client.set(cache_key, "seen", ex=300)
        except:
            pass

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

    latency = round(time.time() - start, 4)

    return {
        "risk": final_risk,
        "ml_score": ml_risk,
        "rules_triggered": rules_triggered,
        "latency": latency,
        "cache_hit": cache_hit
    }


@app.get("/transactions", response_model=List[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


app.include_router(fraud_rules_router)
