from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    fullname: Optional[str] = None
    location: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
