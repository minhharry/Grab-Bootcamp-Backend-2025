from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class RestaurantModel(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_name = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True) 
    restaurant_description = Column(Text, nullable=True) 
    opening_hours = Column(Text, nullable=True) 
    price_range = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    source = Column(Text, nullable=True) 
    restaurant_rating = Column(Float, nullable=True)
    restaurant_rating_count = Column(Integer, nullable=True)
    restaurant_url = Column(Text, nullable=True)
    crawl_time = Column(DateTime, nullable=True) 
    crawl_id = Column(Text, nullable=True)


    images = relationship("ImageModel", back_populates="restaurant")
    reviews = relationship("ReviewModel", back_populates="restaurant")


class ImageModel(Base):
    __tablename__ = "images"

    img_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(PG_UUID(as_uuid=True), ForeignKey('restaurants.restaurant_id'), nullable=True)
    food_name = Column(Text, nullable=True)
    food_price = Column(Text, nullable=True)
    img_url = Column(Text, nullable=True)

    restaurant = relationship("RestaurantModel", back_populates="images")


class ReviewModel(Base):
    __tablename__ = "reviews"

    review_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(PG_UUID(as_uuid=True), ForeignKey('restaurants.restaurant_id'), nullable=True)
    user_rating = Column(Float, nullable=True)
    user_review = Column(Text, nullable=True)
    review_user_name = Column(Text, nullable=True)
    review_date	= Column(Text, nullable=True)

    restaurant = relationship("RestaurantModel", back_populates="reviews")

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True, unique=True, index=True)
    password_hash = Column(String(255), nullable=True)

    # profile = relationship("UserProfileModel", back_populates="user", uselist=False, cascade="all, delete")


# class UserProfileModel(Base):
#     __tablename__ = "user_profiles"

#     user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
#     location = Column(String(100), nullable=True)
#     preference = Column(String, nullable=True)
#     gender = Column(String, nullable=True)
#     date_of_birth = Column(Date, nullable=True)

#     user = relationship("UserModel", back_populates="profile")