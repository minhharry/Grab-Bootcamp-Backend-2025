from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class Review(BaseModel):
    review_id: UUID
    user_rating: Optional[float] = None
    user_review: Optional[str] = None
    review_user_name: Optional[str] = None
    review_date: Optional[str] = None

class FoodItem(BaseModel):
    img_id: UUID
    food_name: Optional[str] = None
    food_price: Optional[str] = None
    img_url: Optional[str] = None

class RestaurantDetail(BaseModel):
    restaurant_id: UUID
    restaurant_name: Optional[str]
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    restaurant_description: Optional[str] = None
    opening_hours: Optional[str] = None
    price_range: Optional[str] = None
    restaurant_rating: Optional[float] = None
    restaurant_rating_count: Optional[int] = None
    restaurant_url: Optional[str] = None
    food_items: List[FoodItem] = []
    reviews: List[Review] = []