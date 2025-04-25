from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class ImageResult(BaseModel):
    score: float

    img_id: Optional[UUID]
    restaurant_id: Optional[UUID]
    food_name: Optional[str]
    food_price: Optional[str]
    img_url: Optional[str]
    
    restaurant_name: Optional[str]
    address: Optional[str]
    restaurant_rating: Optional[float]
    restaurant_url: Optional[str]

class SearchResponse(BaseModel):
    results: List[ImageResult]