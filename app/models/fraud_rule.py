from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class FraudRule(Base):
    __tablename__ = "fraud_rules"

    id = Column(Integer, primary_key=True)
    field = Column(String, nullable=False)
    operator = Column(String, nullable=False)
    value = Column(String, nullable=False)
    active = Column(Boolean, default=True)
