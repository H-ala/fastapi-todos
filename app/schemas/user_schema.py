from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=3)
    last_name: Optional[str] = Field(None, min_length=3)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=3)
    repeat_password: str = Field(..., min_length=3)


class UserUpdateRequest(BaseModel):
    first_name: str | None = Field(default=None, min_length=3)
    last_name: str | None = Field(default=None, min_length=3)
    username: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None, min_length=3)
    repeat_password: str | None = Field(default=None, min_length=3)


class UserOut(BaseModel):
    first_name: Optional[str] = Field(None, min_length=3)
    last_name: Optional[str] = Field(None, min_length=3)
    username: str = Field(..., min_length=3)
    email: EmailStr = Field(...)
    
