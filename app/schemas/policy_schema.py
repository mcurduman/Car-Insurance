from pydantic import BaseModel
from typing import Optional
from datetime import date

class InsurancePolicyBase(BaseModel):
    car_id: int
    provider: Optional[str] = None
    start_date: date
    end_date: date
    logged_expiry_at: Optional[date] = None

    class Config:
        orm_mode = True