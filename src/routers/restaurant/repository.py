from sqlalchemy.orm import Session
from models import RestaurantModel, ImageModel, ReviewModel

def extract_price_level(value):
    if not isinstance(value, str) or value.strip().lower() in ['null', 'n/a', '']:
        return None
    try:
        parts = value.split('-')
        upper_str = parts[-1].strip().replace('.', '')
        upper = int(upper_str)
        if upper > 150000:
            return 3
        elif 50000 < upper <= 150000:
            return 2
        else:
            return 1
    except:
        return None
    
def get_restaurant_detail(db: Session, restaurant_id: str) -> dict | None:
    restaurant = db.query(RestaurantModel).filter_by(restaurant_id=restaurant_id).first()

    if not restaurant:
        return None

    return {
        "restaurant_id": restaurant.restaurant_id,
        "restaurant_name": restaurant.restaurant_name,
        "avatar_url": restaurant.avatar_url,
        "address": restaurant.address,
        "restaurant_description": restaurant.restaurant_description,
        "opening_hours": restaurant.opening_hours,
        "price_level": extract_price_level(restaurant.price_range),
        "restaurant_rating": restaurant.restaurant_rating,
        "restaurant_rating_count": restaurant.restaurant_rating_count,
        "restaurant_url": restaurant.restaurant_url,
    }

def get_restaurant_dishes(db: Session, restaurant_id: str, skip: int, limit: int):
    query = db.query(ImageModel).filter_by(restaurant_id=restaurant_id)
    total = query.count()
    dishes = query.offset(skip).limit(limit).all()

    result = [
        {
            "item_name": d.food_name,
            "item_price": d.food_price,
            "img_item_url": d.img_url,
        }
        for d in dishes
    ]

    return result, total


def get_restaurant_reviews(db: Session, restaurant_id: str, skip: int, limit: int):
    query = db.query(ReviewModel).filter_by(restaurant_id=restaurant_id)
    total = query.count()
    reviews = query.offset(skip).limit(limit).all()


    result = [
        {
            "user_rating": r.user_rating,
            "user_review": r.user_review,
            "review_user_name": r.review_user_name,
            "review_date": r.review_date,
        }
        for r in reviews
    ]

    return result, total