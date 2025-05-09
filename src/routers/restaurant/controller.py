from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from .service import fetch_restaurant_detail, fetch_restaurant_dishes, fetch_restaurant_reviews
from common_schemas.response import ApiResponse, Metadata
from database import get_db

router = APIRouter()

# Endpoint to get restaurant details
@router.get("/{restaurant_id}", response_model=ApiResponse)
def get_restaurant_info(restaurant_id: UUID, db: Session = Depends(get_db)) -> ApiResponse:
    """
    Endpoint to retrieve detailed information about a restaurant.
    Returns the restaurant details along with metadata (if necessary).
    
    Args:
        restaurant_id (UUID): The unique identifier of the restaurant.
        db (Session): Database session for querying.

    Returns:
        ApiResponse: The restaurant's data and metadata.
    """
    data = fetch_restaurant_detail(restaurant_id, db)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Restaurants not found"
        )
    
    return ApiResponse(
        status=200,
        message="Data details retrieved successfully",
        data=data, 
        metadata=None  # No pagination for this route
    )

# Endpoint to get paginated dishes for a restaurant
@router.get("/{restaurant_id}/dishes", response_model=ApiResponse)
def get_restaurant_dishes(
    restaurant_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint to retrieve a paginated list of dishes from a restaurant.
    Returns the dishes with pagination metadata.

    Args:
        restaurant_id (UUID): The unique identifier of the restaurant.
        page (int): The page number for pagination.
        page_size (int): Number of items per page.
        db (Session): Database session for querying.

    Returns:
        ApiResponse: List of dishes and pagination metadata.
    """
    data = fetch_restaurant_dishes(restaurant_id, db, page, page_size)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Dishes not found"
        )

    return ApiResponse(
        status=200,
        message="Data retrieved successfully",
        data=data['dishes'],  # A list of FoodItem models
        metadata=Metadata(
            page=data['page'],
            size=data['page_size'],
            total=data['total_items']
        )
    )

# Endpoint to get paginated reviews for a restaurant
@router.get("/{restaurant_id}/reviews", response_model=ApiResponse)
def get_restaurant_reviews(
    restaurant_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint to retrieve a paginated list of user reviews for a restaurant.
    Returns the reviews with pagination metadata.

    Args:
        restaurant_id (UUID): The unique identifier of the restaurant.
        page (int): The page number for pagination.
        page_size (int): Number of items per page.
        db (Session): Database session for querying.

    Returns:
        ApiResponse: List of reviews and pagination metadata.
    """
    data = fetch_restaurant_reviews(restaurant_id, db, page, page_size)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Reviews not found"
        )

    return ApiResponse(
        status=200,
        message="Data retrieved successfully",
        data=data['reviews'],  # A list of Review models
        metadata=Metadata(
            page=data['page'],
            size=data['page_size'],
            total=data['total_reviews']
        )
    )
