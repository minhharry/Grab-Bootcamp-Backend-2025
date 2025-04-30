from sqlalchemy.orm import Session
from .model import RestaurantDetail, FoodItem, Review, PaginatedDishes, PaginatedReviews
from .repository import get_restaurant_detail, get_restaurant_dishes, get_restaurant_reviews
import math



def fetch_restaurant_detail(restaurant_id: str, db: Session) -> RestaurantDetail | None:
    raw_data = get_restaurant_detail(db, restaurant_id)

    if not raw_data:
        return None


    return RestaurantDetail(
        restaurant_id=raw_data["restaurant_id"],
        restaurant_name=raw_data.get("restaurant_name"),
        avatar_url=raw_data.get("avatar_url"),
        address=raw_data.get("address"),
        restaurant_description=raw_data.get("restaurant_description"),
        opening_hours=raw_data.get("opening_hours"),
        price_level=raw_data.get("price_level"),
        restaurant_rating=raw_data.get("restaurant_rating"),
        restaurant_rating_count=raw_data.get("restaurant_rating_count"),
        restaurant_url=raw_data.get("restaurant_url"),
    )

def fetch_restaurant_dishes(restaurant_id: str, db: Session, page: int, page_size: int) -> PaginatedDishes | None:
    skip = (page - 1) * page_size
    data, total = get_restaurant_dishes(db, restaurant_id, skip, page_size)
    if data is None:
        return None

    total_pages = math.ceil(total / page_size)
    return PaginatedDishes(
        restaurant_id=restaurant_id,
        total_items=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        dishes=[FoodItem.model_validate(d) for d in data]
    )


def fetch_restaurant_reviews(restaurant_id: str, db: Session, page: int, page_size: int) -> PaginatedReviews | None:
    skip = (page - 1) * page_size
    data, total = get_restaurant_reviews(db, restaurant_id, skip, page_size)
    if data is None:
        return None

    total_pages = math.ceil(total / page_size)
    return PaginatedReviews(
        restaurant_id=restaurant_id,
        total_reviews=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        reviews=[Review.model_validate(r) for r in data]
    )