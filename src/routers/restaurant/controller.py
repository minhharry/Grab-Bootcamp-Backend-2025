from .service import fetch_restaurant_detail
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from .model import RestaurantDetail

router = APIRouter()
@router.get("/restaurant/{restaurant_id}", response_model=RestaurantDetail)
def get_restaurant_info(restaurant_id: str, db: Session = Depends(get_db)):
    data = fetch_restaurant_detail(restaurant_id, db)
    if not data:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return data
