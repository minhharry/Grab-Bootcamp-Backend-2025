from sqlalchemy.orm import Session, joinedload
from typing import List, Dict
from models import ImageModel

def get_image_restaurant_data(db: Session, img_ids: List[str]) -> Dict[str, dict]:
    results = (
        db.query(ImageModel)
        .options(joinedload(ImageModel.restaurant))
        .filter(ImageModel.img_id.in_(img_ids))
        .all()
    )

    data = {}
    for img in results:
        rest = img.restaurant
        data[str(img.img_id)] = {
            "img_id": img.img_id,
            "restaurant_id": img.restaurant_id,
            "food_name": img.food_name,
            "food_price": img.food_price,
            "img_url": img.img_url,
            "restaurant_name": rest.restaurant_name if rest else None,
            "avatar_url": rest.avatar_url if rest else None,
            "address": rest.address if rest else None,
            "restaurant_rating": rest.restaurant_rating if rest else None,
            "restaurant_url": rest.restaurant_url if rest else None,
            "restaurant_description": rest.restaurant_description if rest else None,
        }

    return data
