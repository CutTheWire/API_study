from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: str
    pw: str
    user_name: str
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    user_idx: int
    user_id: str
    user_name: str
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True
