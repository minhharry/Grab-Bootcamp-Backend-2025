from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ImageResultItem(BaseModel):
    score: float
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
    distance: Optional[float] = None

