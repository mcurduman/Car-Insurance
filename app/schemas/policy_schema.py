from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class InsurancePolicyBase(BaseModel):
    car_id: int
    provider: Optional[str] = None
    start_date: date
    end_date: date
    logged_expiry_at: Optional[date] = None
    model_config = { "from_attributes": True }

class InsurancePolicyCreate(InsurancePolicyBase):
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: date, values) -> date:
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError("end_date must be after start_date")
        return v

class InsurancePolicyResponse(InsurancePolicyBase):
    id: int

class InsurancePolicyUpdate(BaseModel):
    provider: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    logged_expiry_at: Optional[date] = None

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], values) -> Optional[date]:
        if v is not None and 'start_date' in values and values['start_date'] is not None:
            if v <= values['start_date']:
                raise ValueError("end_date must be after start_date")
        return v
    