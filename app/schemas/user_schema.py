
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str = Field(alias="username")
    email: EmailStr = Field(alias="email")

class UserCreate(UserBase):
    password: str = Field(alias="password")

class User(UserBase):
    id: int = Field(alias="id")
    full_name: str = Field(alias="fullName")
    is_active: bool = Field(alias="isActive")
    is_superuser: bool = Field(alias="isSuperuser")

    model_config = {"from_attributes": True, "populate_by_name": True}

class LoginData(BaseModel):
    username: str = Field(alias="username")
    password: str = Field(alias="password")

class Token(BaseModel):
    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType")

class TokenData(BaseModel):
    username: str | None = Field(default=None, alias="username")
