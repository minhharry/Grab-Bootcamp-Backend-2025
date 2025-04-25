from sqlalchemy.orm import Session
from sqlalchemy import text

def get_restaurant_detail(db: Session, restaurant_id: str) -> dict:
    restaurant_query = text("SELECT * FROM restaurants WHERE restaurant_id = :id")
    restaurant = db.execute(restaurant_query, {"id": restaurant_id}).fetchone()

    if not restaurant:
        return None

    food_items_query = text("SELECT * FROM images WHERE restaurant_id = :id")
    food_items = db.execute(food_items_query, {"id": restaurant_id}).fetchall()

    reviews_query = text("SELECT * FROM reviews WHERE restaurant_id = :id")
    reviews = db.execute(reviews_query, {"id": restaurant_id}).fetchall()

    return {
        "restaurant_id": restaurant.restaurant_id,
        "restaurant_name": restaurant.restaurant_name,
        "address": restaurant.address,
        "restaurant_rating": restaurant.restaurant_rating,
        "restaurant_rating_count": restaurant.restaurant_rating_count,  
        "restaurant_url": restaurant.restaurant_url,
        "food_items": [dict(row._mapping) for row in food_items],
        "reviews": [dict(row._mapping) for row in reviews],
    }
