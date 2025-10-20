from pydantic import BaseModel
from typing import Optional

class CarBase(BaseModel):
    vin: str
    make: Optional[str] = None
    model: Optional[str] = None
    year_of_manufacture: Optional[int] = None
    owner_id: int

    class Config:
        orm_mode = True
