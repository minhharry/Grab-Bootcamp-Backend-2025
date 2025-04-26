from sqlalchemy.orm import Session
from .model import RestaurantDetail, FoodItem, Review
from .repository import get_restaurant_detail


def fetch_restaurant_detail(restaurant_id: str, db: Session) -> RestaurantDetail | None:
    raw_data = get_restaurant_detail(db, restaurant_id)

    if not raw_data:
        return None

    food_items = [
        FoodItem(
            img_id=item["img_id"],
            food_name=item.get("food_name"),
            food_price=item.get("food_price"),
            img_url=item.get("img_url")
        )
        for item in raw_data["food_items"]
    ]

    reviews = [
        Review(
            review_id=rev["review_id"],
            user_rating=rev.get("user_rating"),
            user_review=rev.get("user_review")
        )
        for rev in raw_data["reviews"]
    ]

    return RestaurantDetail(
        restaurant_id=raw_data["restaurant_id"],
        restaurant_name=raw_data.get("restaurant_name"),
        avatar_url=raw_data.get("avatar_url"),
        address=raw_data.get("address"),
        restaurant_description=raw_data.get("restaurant_description"),
        opening_hours=raw_data.get("opening_hours"),
        price_range=raw_data.get("price_range"),
        restaurant_rating=raw_data.get("restaurant_rating"),
        restaurant_rating_count=raw_data.get("restaurant_rating_count"),
        restaurant_url=raw_data.get("restaurant_url"),
        food_items=food_items,
        reviews=reviews
    )
