from pydantic import BaseModel

class FraudRuleCreate(BaseModel):
    field: str
    operator: str
    value: str
    active: bool = True

class FraudRuleOut(FraudRuleCreate):
    id: int

    class Config:
        from_attributes = True
