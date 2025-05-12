from sqlalchemy.orm import Session
from models import ImageModel
from uuid import UUID
from typing import Optional

def get_dish_by_img_id(db: Session, img_id: UUID) -> Optional[ImageModel]:
    """
    Fetches the dish information by the image ID (img_id).

    Args:
        db (Session): The database session.
        img_id (UUID): The image ID of the dish.

    Returns:
        ImageModel | None: The dish information if found, else None.
    """
    return db.query(ImageModel).filter(ImageModel.img_id == img_id).first()