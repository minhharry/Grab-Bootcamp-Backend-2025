from sqlalchemy.orm import Session
from .model import RestaurantDetailResponse, FoodItem, ReviewItem
from .repository import get_restaurant_detail, get_restaurant_dishes, get_restaurant_reviews
import math
from typing import List, Dict, Union
from geopy.distance import geodesic

def fetch_restaurant_detail(
    restaurant_id: str, 
    db: Session, 
    user_lat: float = 10.768778567106164, 
    user_long: float = 106.74621772556752
) -> RestaurantDetailResponse | None:
    """
    Fetches restaurant details from the database.
    
    Args:
        restaurant_id (str): Unique identifier of the restaurant.
        db (Session): The database session to interact with the DB.
    
    Returns:
        RestaurantDetailResponse: The restaurant details or None if not found.
    """
    raw_data = get_restaurant_detail(db, restaurant_id)
    if not raw_data:
        return None

    return RestaurantDetailResponse(
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
        distance=geodesic((raw_data.get("latitude", 0), raw_data.get("longitude", 0)), (user_lat, user_long)).km
    )

def fetch_restaurant_dishes(restaurant_id: str, db: Session, page: int, page_size: int) -> Dict[str, Union[List[FoodItem], int]]:
    """
    Fetches a paginated list of dishes for a specific restaurant.
    
    Args:
        restaurant_id (str): Unique identifier of the restaurant.
        db (Session): The database session to interact with the DB.
        page (int): Current page for pagination.
        page_size (int): Number of items per page.
    
    Returns:
        dict: A dictionary containing paginated data of dishes.
    """
    skip = (page - 1) * page_size
    data, total = get_restaurant_dishes(db, restaurant_id, skip, page_size)
    if data is None:
        return None

    total_pages = math.ceil(total / page_size)
    return {
        "dishes": [FoodItem.model_validate(d) for d in data],
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": total_pages
    }

def fetch_restaurant_reviews(restaurant_id: str, db: Session, page: int, page_size: int) -> Dict[str, Union[List[ReviewItem], int]]:
    """
    Fetches a paginated list of reviews for a specific restaurant.
    
    Args:
        restaurant_id (str): Unique identifier of the restaurant.
        db (Session): The database session to interact with the DB.
        page (int): Current page for pagination.
        page_size (int): Number of items per page.
    
    Returns:
        dict: A dictionary containing paginated data of reviews.
    """
    skip = (page - 1) * page_size
    data, total = get_restaurant_reviews(db, restaurant_id, skip, page_size)
    if data is None:
        return None

    total_pages = math.ceil(total / page_size)
    return {
        "reviews": [ReviewItem.model_validate(r) for r in data],
        "page": page,
        "page_size": page_size,
        "total_reviews": total,
        "total_pages": total_pages
    }

