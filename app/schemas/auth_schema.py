from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class RefreshToken(BaseModel):
    user_id: int = Field(..., gt=0)
    jti: str = Field(..., min_length=64, max_length=100)
    expires_at: datetime = Field(...)
    revoked: bool = Field(False)
    replaced_by: Optional[str] = Field(None, min_length=64, max_length=100)

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=64, max_length=100)


