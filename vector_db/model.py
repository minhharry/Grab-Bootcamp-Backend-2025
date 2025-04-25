from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid

class ImageModel(Base):
    __tablename__ = "images"

    img_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), nullable=True)
    food_name = Column(Text, nullable=True)
    food_price = Column(Text, nullable=True)
    img_url = Column(Text, nullable=True)
