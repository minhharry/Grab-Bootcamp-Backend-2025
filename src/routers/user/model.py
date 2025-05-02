from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class UserProfile(BaseModel):
    user_id: UUID
    location: Optional[str] = None
    preference: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserPreferenceUpdate(BaseModel):
    preference: Optional[str] = None  
