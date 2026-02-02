from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.fraud_rule import FraudRule
from app.schemas.fraud_rule import FraudRuleCreate, FraudRuleOut

router = APIRouter(prefix="/fraud-rules", tags=["Fraud Rules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FraudRuleOut)
def create_rule(rule: FraudRuleCreate, db: Session = Depends(get_db)):
    db_rule = FraudRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/", response_model=list[FraudRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(FraudRule).all()
