from sqlalchemy import Column, String, Text, Float, Integer, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy
import uuid

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users' 

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=sqlalchemy.text("gen_random_uuid()"))
    username = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=True)
    
class Restaurants(Base):
    __tablename__ = 'restaurants'
    restaurant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_name = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    restaurant_description = Column(Text, nullable=True)
    opening_hours = Column(Text, nullable=True)
    price_range = Column(JSON, nullable=True)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    source = Column(Text, nullable=False)
    restaurant_rating = Column(Float, nullable=True)
    restaurant_rating_count = Column(Integer, nullable=True)
    restaurant_url = Column(Text, nullable=True)
    crawl_time = Column(TIMESTAMP, nullable=True)
    crawl_id = Column(Text, nullable=True)

class User_restaurant_clicks(Base):
    __tablename__ = 'user_restaurant_clicks'
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.user_id), primary_key=True)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey(Restaurants.restaurant_id), primary_key=True)
    click_count = Column(Integer, nullable=True)