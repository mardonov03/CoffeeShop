from pydantic import BaseModel, constr, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    gmail: EmailStr
    password: constr(min_length=8)
    full_name: str | None = None

class UserSignIn(BaseModel):
    gmail: EmailStr
    password: constr(min_length=8)

class VerifyGmail(BaseModel):
    gmail: EmailStr

class UserInfo(BaseModel):
    userid: int
    gmail: EmailStr
    full_name: str | None = None
    role: str
    added_time: datetime
    account_status: bool
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    gmail: str | None = None
    role: str | None = None