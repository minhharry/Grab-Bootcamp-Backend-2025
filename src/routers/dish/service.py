from sqlalchemy.orm import Session
from uuid import UUID
from .repository import get_dish_by_img_id
from .model import Dish
from fastapi import HTTPException

def fetch_dish_by_img_id(db: Session, img_id: UUID) -> Dish:
    """
    Fetches the dish information by image ID and returns it as a Pydantic model.

    Args:
        db (Session): The database session.
        img_id (UUID): The image ID of the dish.

    Returns:
        Dish: The Pydantic model containing dish details.
    
    Raises:
        HTTPException: If no dish is found for the given img_id.
    """
    dish = get_dish_by_img_id(db, img_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    return Dish(
        img_id=dish.img_id,
        food_name=dish.food_name,
        food_price=dish.food_price,
        img_url=dish.img_url,
        restaurant_id=dish.restaurant_id
    )