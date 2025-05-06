from sqlalchemy.orm import Session
from models import UserModel
from .model import UserSignup
import uuid

def get_user_by_email(db: Session, email: str) -> UserModel | None:
    """
    Fetch a user by email from the database.

    Args:
        db (Session): The database session to interact with the DB.
        email (str): The email to search for.

    Returns:
        UserModel | None: The user object if found, None otherwise.
    """
    return db.query(UserModel).filter_by(email=email).first()

def get_user_by_id(db: Session, user_id: str) -> UserModel | None:
    """
    Fetch a user by user ID from the database.

    Args:
        db (Session): The database session to interact with the DB.
        user_id (str): The unique user ID to search for.

    Returns:
        UserModel | None: The user object if found, None otherwise.
    """
    return db.query(UserModel).filter_by(user_id=user_id).first()

def create_user_with_profile(db: Session, user: UserSignup, hashed_password: str) -> UserModel:
    """
    Create a new user along with their profile and save them to the database.

    Args:
        db (Session): The database session to interact with the DB.
        user (UserSignup): The data from the user signup form.
        hashed_password (str): The hashed password to store.

    Returns:
        UserModel: The newly created user object.
    """
    user_id = uuid.uuid4()
    
    # Create the user object
    db_user = UserModel(
        user_id=user_id,
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )
    db.add(db_user)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)

    return db_user
