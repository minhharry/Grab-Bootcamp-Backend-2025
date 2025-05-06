from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class UserRestaurantClickModel(Base):
    __tablename__ = 'user_restaurant_clicks'

    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    restaurant_id = Column(PG_UUID(as_uuid=True), ForeignKey('restaurants.restaurant_id', ondelete='CASCADE'), primary_key=True)
    click_count = Column(Integer, default=1) 

    user = relationship("UserModel", back_populates="user_restaurant_clicks")

    restaurant = relationship("RestaurantModel", back_populates="user_restaurant_clicks")
