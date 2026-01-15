from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, Transaction
from app.schemas import TransactionCreate
from app.celery_worker import fraud_alert

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelStream")

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
    risk = "LOW"

    if txn.amount > 5000:
        risk = "HIGH"
        fraud_alert.delay(txn.dict())

    record = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        risk=risk
    )

    db.add(record)
    db.commit()

    return {"risk": risk}
