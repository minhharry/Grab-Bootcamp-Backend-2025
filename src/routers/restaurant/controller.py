from .service import fetch_restaurant_detail, fetch_restaurant_dishes, fetch_restaurant_reviews
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from .model import RestaurantDetail, PaginatedReviews, PaginatedDishes
from uuid import UUID

router = APIRouter()

@router.get("/{restaurant_id}", response_model=RestaurantDetail)
def get_restaurant_info(restaurant_id: UUID, db: Session = Depends(get_db)):
    data = fetch_restaurant_detail(restaurant_id, db)
    if not data:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return data

@router.get("/{restaurant_id}/dishes", response_model=PaginatedDishes)
def get_restaurant_dishes(
    restaurant_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    data = fetch_restaurant_dishes(str(restaurant_id), db, page, page_size)
    if not data:
        raise HTTPException(status_code=404, detail="Dishes not found")
    return data

@router.get("/{restaurant_id}/reviews", response_model=PaginatedReviews)
def get_restaurant_reviews(
    restaurant_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    data = fetch_restaurant_reviews(str(restaurant_id), db, page, page_size)
    if not data:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return data
