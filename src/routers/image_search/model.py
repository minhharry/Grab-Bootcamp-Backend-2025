from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class ImageResult(BaseModel):
    score: float

    img_id: Optional[UUID]
    restaurant_id: Optional[UUID]
    food_name: Optional[str] = None
    food_price: Optional[str] = None
    img_url: Optional[str] = None
    
    restaurant_name: Optional[str]
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    restaurant_rating: Optional[float] = None
    restaurant_url: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[ImageResult]