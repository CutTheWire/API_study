from typing import Optional
from pydantic import BaseModel


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

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class ThroughputDayAllResponse(BaseModel):
    id: int
    iotId:str
    measuredWeight:int
    timeStamp:str
    status:bool

class GetDeviceToken(BaseModel):
    iotId: str

    class Config:
        orm_mode = True
