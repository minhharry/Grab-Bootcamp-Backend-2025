from sqlalchemy.orm import Session
from models import RestaurantModel

def get_restaurant_detail(db: Session, restaurant_id: str) -> dict | None:
    restaurant = db.query(RestaurantModel).filter_by(restaurant_id=restaurant_id).first()

    if not restaurant:
        return None

    return {
        "restaurant_id": restaurant.restaurant_id,
        "restaurant_name": restaurant.restaurant_name,
        "address": restaurant.address,
        "restaurant_rating": restaurant.restaurant_rating,
        "restaurant_rating_count": restaurant.restaurant_rating_count,
        "restaurant_url": restaurant.restaurant_url,
        "food_items": [
            {
                "img_id": img.img_id,
                "food_name": img.food_name,
                "food_price": img.food_price,
                "img_url": img.img_url
            } for img in restaurant.images
        ],
        "reviews": [
            {
                "review_id": rev.review_id,
                "user_rating": rev.user_rating,
                "user_review": rev.user_review
            } for rev in restaurant.reviews
        ]
    }
