
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from .base import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True, unique=True, index=True)
    password_hash = Column(String(255), nullable=True)
