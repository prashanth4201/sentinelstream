from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import redis
import json

from app.database import SessionLocal
from app.models import Transaction
from app.schemas import TransactionCreate

app = FastAPI(title="SentinelStream")

# Redis connection (Redis already running on localhost:6379)
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

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
    # ---- Redis caching logic (Week-2 requirement) ----
    cache_key = f"user:{txn.user_id}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        user_data = json.loads(cached_user)
        cache_hit = True
    else:
        user_data = {"user_id": txn.user_id}
        redis_client.set(cache_key, json.dumps(user_data), ex=300)
        cache_hit = False
    # -------------------------------------------------

    # Business logic
    risk = "LOW"
    if txn.amount > 5000:
        risk = "HIGH"

    # Store transaction in DB
    record = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        risk=risk
    )

    db.add(record)
    db.commit()

    return {
        "risk": risk,
        "cached": cache_hit
    }
