from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class ImageModel(Base):
    __tablename__ = "images"

    img_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(PG_UUID(as_uuid=True), ForeignKey("restaurants.restaurant_id"), nullable=True)
    food_name = Column(Text, nullable=True)
    food_price = Column(Text, nullable=True)
    img_url = Column(Text, nullable=True)

    restaurant = relationship("RestaurantModel", back_populates="images")
