from sqlalchemy.orm import Session
from models import UserRestaurantClickModel, RestaurantModel
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Optional
from utils import extract_price_level
from sqlalchemy import func
from sqlalchemy import text


    
def get_user_restaurant_clicks_by_restaurant(db: Session, user_id: str, restaurant_id: str):
    """
    Fetches the existing click record for a given user and restaurant.
    
    Args:
        db: Database session
        user_id: User's UUID
        restaurant_id: Restaurant's UUID
        
    Returns:
        UserRestaurantClickModel | None: The click record or None if not found.
    """
    return db.query(UserRestaurantClickModel).filter_by(user_id=user_id, restaurant_id=restaurant_id).first()

def get_user_clicks(db: Session) -> Optional[List[UserRestaurantClickModel]]:
    """
    Fetches the existing click record all user.
    
    Args:
        db: Database session
        
    Returns:
        List[UserRestaurantClickModel] | None: The click record or None if not found.
    """
    return db.query(UserRestaurantClickModel).all()

def add_click(db: Session, user_id: str, restaurant_id: str) -> bool:
    """
    Adds a new click entry or updates the click count if the user has already clicked the restaurant.
    
    Args:
        db: Database session
        user_id: User's UUID
        restaurant_id: Restaurant's UUID
        
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    try:
        click_record = get_user_restaurant_clicks_by_restaurant(db, user_id, restaurant_id)
        
        if click_record:
            # If record exists, increment the click count
            click_record.click_count += 1
        else:
            # Create a new click record
            click_record = UserRestaurantClickModel(user_id=user_id, restaurant_id=restaurant_id, click_count=1)
            db.add(click_record)
        
        db.commit()
        db.refresh(click_record)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        return False
    
def get_restaurants_by_ids(db: Session, restaurant_ids: List) -> Dict[str, Dict]:
    """
    Fetches restaurant details for a list of restaurant_ids.
    
    Args:
        db: Database session
        restaurant_ids: List of restaurant UUIDs to fetch details for
    
    Returns:
        Dictionary where keys are restaurant_ids and values are the restaurant details.
    """
    restaurants = db.query(RestaurantModel).filter(RestaurantModel.restaurant_id.in_(restaurant_ids)).all()
    
 
    data_map = {}
    for restaurant in restaurants:
        data_map[str(restaurant.restaurant_id)] = {
            "restaurant_id": str(restaurant.restaurant_id),
            "restaurant_name": restaurant.restaurant_name,
            "avatar_url": restaurant.avatar_url,
            "address": restaurant.address,
            "price_level": extract_price_level(restaurant.price_range),  
            "restaurant_rating": restaurant.restaurant_rating,
            "longitude": restaurant.longitude,
            "latitude": restaurant.latitude
        }
    
    return data_map


def get_random_restaurants(db: Session, limit: int = 10) -> List[Dict]:
    """
    Fetches a random list of restaurants from the database and returns them with price levels.

    Args:
        db (Session): The database session.
        limit (int): The number of random restaurants to fetch (default is 10).

    Returns:
        list: A list of restaurant objects with their details and price level.
    """
    query = text("""
            SELECT * FROM restaurants
            TABLESAMPLE SYSTEM (15)  
            LIMIT :limit;           
        """)

    result = db.execute(query, {"limit": limit})

    restaurants = result.fetchall()

    if not restaurants:
        return []

    data = []
    for restaurant in restaurants:
        data.append({
            "restaurant_id": str(restaurant.restaurant_id),
            "restaurant_name": restaurant.restaurant_name,
            "avatar_url": restaurant.avatar_url,
            "address": restaurant.address,
            "price_level": extract_price_level(restaurant.price_range), 
            "restaurant_rating": restaurant.restaurant_rating,
            "longitude": restaurant.longitude,
            "latitude": restaurant.latitude
        })

    return data