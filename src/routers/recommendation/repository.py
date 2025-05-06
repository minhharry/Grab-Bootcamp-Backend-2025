from sqlalchemy.orm import Session
from models import UserRestaurantClickModel
from sqlalchemy.exc import SQLAlchemyError

def get_user_restaurant_click(db: Session, user_id: str, restaurant_id: str):
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
        click_record = get_user_restaurant_click(db, user_id, restaurant_id)
        
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