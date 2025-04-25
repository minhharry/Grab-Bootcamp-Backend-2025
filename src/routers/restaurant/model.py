from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class Review(BaseModel):
    review_id: UUID
    user_rating: Optional[float]
    user_review: Optional[str]

class FoodItem(BaseModel):
    img_id: UUID
    food_name: Optional[str]
    food_price: Optional[str]
    img_url: Optional[str]

class RestaurantDetail(BaseModel):
    restaurant_id: UUID
    restaurant_name: Optional[str]
    address: Optional[str]
    restaurant_rating: Optional[float]
    restaurant_rating_count: Optional[int]
    restaurant_url: Optional[str]
    food_items: List[FoodItem] = []
    reviews: List[Review] = []
