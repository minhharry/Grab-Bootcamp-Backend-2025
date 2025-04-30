from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class ImageResult(BaseModel):
    score: float
    restaurant_id: Optional[UUID]
    restaurant_name: Optional[str]
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    restaurant_rating: Optional[float] = None
    price_level: Optional[int] = None

class SearchResponse(BaseModel):
    results: List[ImageResult]