from pydantic import BaseModel, field_validator
from typing import Optional

class OwnerBase(BaseModel):
    name: str
    email: Optional[str] = None
    model_config = { "from_attributes": True }
    
class OwnerCreate(OwnerBase):
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and "@" not in v:
            raise ValueError("Invalid email address")
        return v
    

class OwnerResponse(OwnerBase):
    id: int


class OwnerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
