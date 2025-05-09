from sqlalchemy.orm import Session, joinedload
from typing import List
from models import ImageModel
from .model import ImageResultItem 
from utils import extract_price_level

    
def get_image_restaurant_data(db: Session, img_ids: List[str]) -> List[ImageResultItem]:
    """
    Retrieves image data from the database and maps it to the restaurant data.

    Args:
        db (Session): The database session to interact with the DB.
        img_ids (List[str]): List of image IDs to retrieve corresponding restaurant data.

    Returns:
        List[SearchResultItem]: A list of `SearchResultItem` containing restaurant and image data.
    """
    results = (
        db.query(ImageModel)
        .options(joinedload(ImageModel.restaurant))
        .filter(ImageModel.img_id.in_(img_ids))
        .all()
    )

    data = {}
    for img in results:
        rest = img.restaurant
        if rest:
            price_level = extract_price_level(rest.price_range)
            data[str(img.img_id)] = {
                "restaurant_id": img.restaurant_id,
                "restaurant_name": rest.restaurant_name if rest else None,
                "avatar_url": rest.avatar_url if rest else None,
                "address": rest.address if rest else None,
                "price_level": price_level,
                "restaurant_rating": rest.restaurant_rating if rest else None,
                "longitude": rest.longitude if rest else None,
                "latitude": rest.latitude if rest else None
            }


    return data
