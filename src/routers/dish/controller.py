from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .service import fetch_dish_by_img_id
from common_schemas.response import ApiResponse
from database import get_db

router = APIRouter()

@router.get("/{img_id}", response_model=ApiResponse, tags = ["Dish Information"])
def get_dish(img_id: UUID, db: Session = Depends(get_db)) -> ApiResponse:
    """
    Endpoint to retrieve dish information by img_id.

    Args:
        img_id (UUID): The image ID of the dish.
        db (Session): The database session to interact with the DB.

    Returns:
        ApiResponse: The dish information in standardized response format.
    """
    try:
        dish = fetch_dish_by_img_id(db, img_id)
        return ApiResponse(
            status=200,
            message="Data retrieved successfully",
            data=dish, 
            metadata=None
        )
    except HTTPException as e:
        raise e