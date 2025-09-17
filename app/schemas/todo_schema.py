from pydantic import BaseModel, Field
from typing import Optional

class TodoRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3, max_length=240)
    priority: Optional[int] = Field(None, gt=0, lt=6)
    complete: bool = Field(...)


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3, max_length=240)
    priority: Optional[int] = Field(None, gt=0, lt=6)
    complete: Optional[bool] = None

class TodoOut(TodoRequest):
    pass