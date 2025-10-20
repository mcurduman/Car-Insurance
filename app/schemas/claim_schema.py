from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ClaimBase(BaseModel):
    car_id: int
    claim_date: date
    description: str
    amount: float

    class Config:
        orm_mode = True