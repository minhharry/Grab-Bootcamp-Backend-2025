from sqlalchemy import Column, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class ReviewModel(Base):
    __tablename__ = "reviews"

    review_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(PG_UUID(as_uuid=True), ForeignKey("restaurants.restaurant_id"), nullable=True)
    user_rating = Column(Float, nullable=True)
    user_review = Column(Text, nullable=True)
    review_user_name = Column(Text, nullable=True)
    review_date = Column(Text, nullable=True)

    restaurant = relationship("RestaurantModel", back_populates="reviews")
