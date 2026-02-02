from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user_id: int
    amount: float

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    risk: str

    class Config:
        from_attributes = True
