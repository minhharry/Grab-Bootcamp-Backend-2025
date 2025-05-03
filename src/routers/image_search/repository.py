from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models import ImageModel
from .model import ImageResultItem 

def extract_price_level(price_range: dict) -> Optional[int]:
    """
    Extracts the price level based on the price_max value in the price_range dictionary.
    Returns an integer representing the price level (1, 2, 3) or None if invalid.

    Args:
        price_range (dict): A dictionary containing 'price_min' and 'price_max'.

    Returns:
        Optional[int]: Price level (1, 2, 3) or None.
    """
    if not isinstance(price_range, dict):
        return None

    # Ensure that the price_range has 'price_max' key and it has a valid value
    price_max = price_range.get("price_max", None)
    if price_max is None:
        return None

    try:
        price_max = float(price_max)
        if price_max > 150000:
            return 3
        elif 50000 < price_max <= 150000:
            return 2
        elif price_max <= 50000:
            return 1
        return None
    except (ValueError, TypeError):
        return None
    
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
            }


    return data
