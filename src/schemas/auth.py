from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str
    fullname: Optional[str] = None
    location: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
