from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import date, datetime
from app.utils.amount import validate_amount

class ClaimBase(BaseModel):
    car_id: int = Field(alias="carId")
    claim_date: date = Field(alias="claimDate")
    description: str = Field(alias="description")
    amount: float = Field(alias="amount")   
    model_config = { "from_attributes": True,
                     "populate_by_name": True }

class ClaimCreate(ClaimBase):
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        return validate_amount(v)

class ClaimResponse(ClaimBase):
    id: int

class ClaimUpdate(BaseModel):
    claim_date: Optional[date] = Field(default=None, alias="claimDate")
    description: Optional[str] = Field(default=None, alias="description")
    amount: Optional[float] = Field(default=None, alias="amount")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            return validate_amount(v)
        return v
        
    
    