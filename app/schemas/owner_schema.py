from pydantic import BaseModel, field_validator, Field, EmailStr
from typing import Optional

class OwnerBase(BaseModel):
    name: str = Field(alias="name")
    email: Optional[EmailStr] = Field(default=None, alias="email")
    model_config = { "from_attributes": True,
                     "populate_by_name": True }
    
class OwnerCreate(OwnerBase):
    pass

class OwnerResponse(OwnerBase):
    id: int = Field(alias="id")


class OwnerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, alias="name")
    email: Optional[str] = Field(default=None, alias="email")
