from pydantic import BaseModel, field_validator, Field
from typing import Optional
from app.utils.dates import validate_year_of_manufacture

from app.schemas.owner_schema import OwnerResponse

class CarBase(BaseModel):
    vin: str = Field(alias="vin")
    make: Optional[str] = Field(default=None, alias="make")
    model: Optional[str] = Field(default=None, alias="model")
    year_of_manufacture: Optional[int] = Field(default=None, alias="yearOfManufacture")
    owner_id: int = Field(alias="ownerId")
    model_config = { "from_attributes": True,
                     "populate_by_name": True }

class CarCreate(CarBase):
    @field_validator('vin')
    @classmethod
    def normalize_vin(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != 17:
            raise ValueError("VIN must be exactly 17 characters long")
        return v

    @field_validator('year_of_manufacture')
    @classmethod
    def validate_year_of_manufacture(cls, v: Optional[int]) -> Optional[int]:
        if v is not None:
            validate_year_of_manufacture(v)
        return v

class CarUpdate(BaseModel):
    vin: str | None = Field(default=None, alias="vin")
    make: Optional[str] = Field(default=None, alias="make")
    model: Optional[str] = Field(default=None, alias="model")
    year_of_manufacture: Optional[int] = Field(default=None, alias="yearOfManufacture")
    owner_id: Optional[int] = Field(default=None, alias="ownerId")

    @field_validator('year_of_manufacture')
    @classmethod
    def validate_year_of_manufacture(cls, v: Optional[int]) -> Optional[int]:
        if v is not None:
            validate_year_of_manufacture(v)
        return v


class CarResponse(CarBase):
    id: int = Field(alias="id")

class CarWithOwnerResponse(CarResponse):
    owner: 'OwnerResponse' = Field(alias="owner")
