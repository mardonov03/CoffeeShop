from pydantic import BaseModel, constr, EmailStr,conint
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    gmail: EmailStr
    password: constr(min_length=8)
    full_name: constr(min_length=1)

class UserLogin(BaseModel):
    gmail: Optional[EmailStr] = None
    password: constr(min_length=8)

class VerifyGmail(BaseModel):
    gmail: EmailStr

class UserInfo(BaseModel):
    userid: int
    gmail: EmailStr
    full_name: str
    role: str
    added_time: datetime
    account_status: bool
