from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from .base import Base

class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    location = Column(String(100), nullable=True)
    preference = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    user = relationship("UserModel", back_populates="profile")