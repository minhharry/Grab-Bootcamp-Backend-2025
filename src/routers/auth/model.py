from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserSignup(BaseModel):
    email: str
    password: str
    username: Optional[str] = None
    location: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str