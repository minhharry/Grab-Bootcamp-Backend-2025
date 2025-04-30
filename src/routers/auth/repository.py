from sqlalchemy.orm import Session
from models import UserModel, UserProfileModel
from .model import UserSignup
import uuid

def get_user_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter_by(email=email).first()

def create_user_with_profile(db: Session, user: UserSignup, hashed_password: str) -> UserModel:
    user_id = uuid.uuid4()
    
    db_user = UserModel(
        user_id=user_id,
        email=user.email,
        fullname=user.fullname,
        password_hash=hashed_password
    )
    db.add(db_user)

    db_profile = UserProfileModel(
        user_id=user_id,
        location=user.location,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
        preference=None
    )
    db.add(db_profile)

    db.commit()
    db.refresh(db_user)
    return db_user