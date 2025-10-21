from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime

class ClaimBase(BaseModel):
    car_id: int
    claim_date: date
    description: str
    amount: float
    model_config = { "from_attributes": True }

class ClaimCreate(ClaimBase):
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Amount must be non-negative")
        return v

class ClaimResponse(ClaimBase):
    id: int

class ClaimUpdate(BaseModel):
    claim_date: Optional[date] = None
    description: Optional[str] = None
    amount: Optional[float] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Amount must be non-negative")
        return v

    
    