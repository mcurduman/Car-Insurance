from pydantic import BaseModel, field_validator
from typing import Optional

class CarBase(BaseModel):
    vin: str
    make: Optional[str] = None
    model: Optional[str] = None
    year_of_manufacture: Optional[int] = None
    owner_id: int
    model_config = { "from_attributes": True }

class CarCreate(CarBase):
    @field_validator('vin')
    @classmethod
    def normalize_vin(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != 17:
            raise ValueError("VIN must be exactly 17 characters long")
        return v

class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year_of_manufacture: Optional[int] = None
    owner_id: Optional[int] = None


class CarResponse(CarBase):
    id: int

    


