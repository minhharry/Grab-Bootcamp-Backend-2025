from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .service import add_click_to_restaurant
from common_schemas.response import ApiResponse
from database import get_db
from uuid import UUID


router = APIRouter()

@router.post("/add-click", response_model=ApiResponse)
def add_click(
    user_id: UUID,
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Endpoint for adding a click from the current user to a specific restaurant.

    Args:
        token (str): The JWT token passed in the Authorization header.
        restaurant_id (UUID): The restaurant's ID
        db (Session): The database session for querying

    Returns:
        ApiResponse: The result of the operation, containing status and message.
    """

    result = add_click_to_restaurant(db, user_id, restaurant_id)
    if result.status != 200:
        raise HTTPException(status_code=result.status, detail=result.message)
    
    return result