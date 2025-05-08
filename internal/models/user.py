from pydantic import BaseModel, constr, EmailStr,conint
from typing import Optional
class UserCreate(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=8)
    gmail: EmailStr
    full_name: constr(min_length=1)

class UserLogin(BaseModel):
    username: Optional[constr(min_length=1)] = None
    password: constr(min_length=8)
    gmail: Optional[EmailStr] = None

class VerifyGmail(BaseModel):
    code: constr(min_length=6)