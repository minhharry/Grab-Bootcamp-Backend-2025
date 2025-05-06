from sqlalchemy.orm import Session
from .repository import add_click
from common_schemas.response import ApiResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def add_click_to_restaurant(db: Session, user_id: str, restaurant_id: str) -> ApiResponse:
    """
    Business logic to handle adding a click for a user to a restaurant.

    Args:
        db: Database session
        user_id: User's UUID
        restaurant_id: Restaurant's UUID

    Returns:
        ApiResponse: The result, containing success or failure status and message.
    """
    if add_click(db, user_id, restaurant_id):
        return ApiResponse(
            status=200,
            message="Click added successfully",
            data=None,
            metadata=None
        )
    else:
        return HTTPException(
            status_code=500,
            detail="Failed to add click"
        )