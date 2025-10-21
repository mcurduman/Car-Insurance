from pydantic import BaseModel, field_validator, Field
from typing import Optional
from app.utils.dates import validate_start_end_dates, validate_start_end_dates_optional
from datetime import date

class InsurancePolicyBase(BaseModel):
    car_id: int = Field(alias="carId")
    provider: Optional[str] = Field(default=None, alias="provider")
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    logged_expiry_at: Optional[date] = Field(default=None, alias="loggedExpiryAt")
    model_config = { "from_attributes": True,
                     "populate_by_name": True }

class InsurancePolicyCreate(InsurancePolicyBase):
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: date, values) -> date:
        validate_start_end_dates(values['start_date'], v)
        return v

class InsurancePolicyResponse(InsurancePolicyBase):
    id: int = Field(alias="id")

class InsurancePolicyUpdate(BaseModel):
    provider: Optional[str] = Field(default=None, alias="provider")
    start_date: Optional[date] = Field(default=None, alias="startDate")
    end_date: Optional[date] = Field(default=None, alias="endDate")
    logged_expiry_at: Optional[date] = Field(default=None, alias="loggedExpiryAt")

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_dates(cls, v: Optional[date], values) -> Optional[date]:
        # Determine which field is being validated and get both dates
        start_date = values.get('start_date') if 'end_date' in values else v
        end_date = values.get('end_date') if 'start_date' in values else v
        validate_start_end_dates_optional(start_date, end_date)
        return v

    