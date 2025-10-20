from pydantic import BaseModel
from typing import Optional

class OwnerBase(BaseModel):
    name: str
    email: Optional[str] = None

    class Config:
        orm_mode = True