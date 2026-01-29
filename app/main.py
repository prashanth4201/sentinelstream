from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import redis
import json

from app.database import SessionLocal
from app.models import Transaction
from app.schemas import TransactionCreate

# Week-3 imports
from app.rules.rule_engine import RuleEngine
from app.workers.celery_worker import send_alert
from app.ml.scoring import ml_score

app = FastAPI(title="SentinelStream")

# Redis connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5
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
    return {"status": "FastAPI running"}

@app.post("/transaction")
def create_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db)
):
    # ---------- Redis caching (Week-2) ----------
    cache_key = f"user:{txn.user_id}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        cache_hit = True
    else:
        redis_client.set(
            cache_key,
            json.dumps({"user_id": txn.user_id}),
            ex=300
        )
        cache_hit = False
    # -------------------------------------------

    # ---------- Week-3 ML + Rule Engine ----------
    ml_risk = ml_score(txn)
    rules_triggered = rule_engine.evaluate(txn)

    final_risk = "LOW"

    # ✅ UPDATED LOGIC (IMPORTANT CHANGE)
    if ml_risk < -0.2 or "HIGH_AMOUNT" in rules_triggered:
        final_risk = "HIGH"
    # --------------------------------------------

    # ---------- Store transaction ----------
    record = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        risk=final_risk
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    # ---------------------------------------

    # ---------- Week-3 Async Alert ----------
    if final_risk == "HIGH":
        send_alert.delay(record.id)
    # ---------------------------------------

    return {
        "risk": final_risk,
        "ml_risk_score": ml_risk,
        "rules_triggered": rules_triggered,
        "cached": cache_hit
    }
