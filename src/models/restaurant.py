from sqlalchemy import Column, Text, Float, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class RestaurantModel(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_name = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    restaurant_description = Column(Text, nullable=True)
    opening_hours = Column(Text, nullable=True)
    price_range = Column(JSON, nullable=True)
    address = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    restaurant_rating = Column(Float, nullable=True)
    restaurant_rating_count = Column(Integer, nullable=True)
    restaurant_url = Column(Text, nullable=True)
    crawl_time = Column(DateTime, nullable=True)
    crawl_id = Column(Text, nullable=True)

    images = relationship("ImageModel", back_populates="restaurant")
    reviews = relationship("ReviewModel", back_populates="restaurant")