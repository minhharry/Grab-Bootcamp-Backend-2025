from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models import ImageModel
from .model import ImageResultItem 

def extract_price_level(value: str) -> Optional[int]:
    """
    Extracts the price level from a string representing a price range.
    Returns an integer representing the price level or None if invalid.

    Args:
        value (str): The price range string.

    Returns:
        Optional[int]: Price level (1, 2, 3) or None.
    """
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
        data[str(img.img_id)] = {
            "restaurant_id": img.restaurant_id,
            "restaurant_name": rest.restaurant_name if rest else None,
            "avatar_url": rest.avatar_url if rest else None,
            "address": rest.address if rest else None,
            "price_level": extract_price_level(rest.price_range if rest else None),
            "restaurant_rating": rest.restaurant_rating if rest else None,
        }

    return data
