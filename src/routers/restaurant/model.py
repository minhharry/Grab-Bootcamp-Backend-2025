from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class Review(BaseModel):
    user_rating: Optional[float] = None
    user_review: Optional[str] = None
    review_user_name: Optional[str] = None
    review_date: Optional[str] = None

class FoodItem(BaseModel):
    item_name: Optional[str] = None
    item_price: Optional[str] = None
    img_item_url: Optional[str] = None

class RestaurantDetail(BaseModel):
    restaurant_id: UUID
    restaurant_name: Optional[str]
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    restaurant_description: Optional[str] = None
    opening_hours: Optional[str] = None
    price_level: Optional[int] = None
    restaurant_rating: Optional[float] = None
    restaurant_rating_count: Optional[int] = None
    restaurant_url: Optional[str] = None

class PaginatedDishes(BaseModel):
    restaurant_id: UUID
    total_items: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    dishes: List[FoodItem]

class PaginatedReviews(BaseModel):
    restaurant_id: UUID
    total_reviews: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    reviews: List[Review]