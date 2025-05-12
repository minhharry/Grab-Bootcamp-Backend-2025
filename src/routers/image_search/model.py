from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from fastapi import UploadFile, File

class ImageResultItem(BaseModel):
    similar_score: float
    final_score: float
    restaurant_id: Optional[UUID]
    restaurant_name: Optional[str]
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    restaurant_rating: Optional[float] = None
    price_level: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    img_id: Optional[UUID] = None 
    food_name: Optional[str] = None  
    food_price: Optional[str] = None  
    img_url: Optional[str] = None

class UserLocation(BaseModel):
    latitude: float
    longitude: float

class ImageSearchRequest(BaseModel):
    user_location: UserLocation
    file: UploadFile = File(...)