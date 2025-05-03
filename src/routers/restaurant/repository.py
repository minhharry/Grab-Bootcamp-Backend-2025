from sqlalchemy.orm import Session
from typing import Optional
from models import RestaurantModel, ImageModel, ReviewModel

def extract_price_level(price_range: dict) -> Optional[int]:
    """
    Extracts the price level based on the price_max value in the price_range dictionary.
    Returns an integer representing the price level (1, 2, 3) or None if invalid.

    Args:
        price_range (dict): A dictionary containing 'price_min' and 'price_max'.

    Returns:
        Optional[int]: Price level (1, 2, 3) or None.
    """
    if not isinstance(price_range, dict):
        return None

    # Ensure that the price_range has 'price_max' key and it has a valid value
    price_max = price_range.get("price_max", None)
    if price_max is None:
        return None

    try:
        price_max = float(price_max)
        if price_max > 150000:
            return 3
        elif 50000 < price_max <= 150000:
            return 2
        elif price_max <= 50000:
            return 1
        return None
    except (ValueError, TypeError):
        return None
    
def get_restaurant_detail(db: Session, restaurant_id: str) -> dict | None:
    """
    Fetches the restaurant details from the database.
    
    Args:
        db (Session): The database session to interact with the DB.
        restaurant_id (str): Unique identifier of the restaurant.
    
    Returns:
        dict: Dictionary of restaurant details or None if not found.
    """
    restaurant = db.query(RestaurantModel).filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return None
    
    price_level = extract_price_level(restaurant.price_range) if restaurant.price_range else None

    return {
        "restaurant_id": restaurant.restaurant_id,
        "restaurant_name": restaurant.restaurant_name,
        "avatar_url": restaurant.avatar_url,
        "address": restaurant.address,
        "restaurant_description": restaurant.restaurant_description,
        "opening_hours": restaurant.opening_hours,
        "price_level": price_level,
        "restaurant_rating": restaurant.restaurant_rating,
        "restaurant_rating_count": restaurant.restaurant_rating_count,
        "restaurant_url": restaurant.restaurant_url,
    }

def get_restaurant_dishes(db: Session, restaurant_id: str, skip: int, limit: int):
    """
    Fetches a paginated list of dishes for a specific restaurant.
    
    Args:
        db (Session): The database session to interact with the DB.
        restaurant_id (str): Unique identifier of the restaurant.
        skip (int): The offset for pagination.
        limit (int): The limit for pagination.
    
    Returns:
        tuple: List of dishes and the total count of dishes.
    """
    query = db.query(ImageModel).filter_by(restaurant_id=restaurant_id)
    total = query.count()
    dishes = query.offset(skip).limit(limit).all()

    result = [
        {
            "item_name": d.food_name,
            "item_price": d.food_price,
            "img_item_url": d.img_url,
        }
        for d in dishes
    ]
    return result, total


def get_restaurant_reviews(db: Session, restaurant_id: str, skip: int, limit: int):
    """
    Fetches a paginated list of reviews for a specific restaurant.
    
    Args:
        db (Session): The database session to interact with the DB.
        restaurant_id (str): Unique identifier of the restaurant.
        skip (int): The offset for pagination.
        limit (int): The limit for pagination.
    
    Returns:
        tuple: List of reviews and the total count of reviews.
    """
    query = db.query(ReviewModel).filter_by(restaurant_id=restaurant_id)
    total = query.count()
    reviews = query.offset(skip).limit(limit).all()

    result = [
        {
            "user_rating": r.user_rating,
            "user_review": r.user_review,
            "review_user_name": r.review_user_name,
            "review_date": r.review_date,
        }
        for r in reviews
    ]

    return result, total
