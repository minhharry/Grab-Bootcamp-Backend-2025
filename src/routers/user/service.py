from sqlalchemy.orm import Session
from .repository import get_user_profile, update_user_profile
from uuid import UUID


def get_profile(db: Session, user_id: UUID) -> dict | None:
    """
    Fetches the user's profile as a dictionary.
    
    Args:
        db: Database session.
        user_id: The ID of the user.
        
    Returns:
        dict: The user's profile data as a dictionary.
    """
    user_profile = get_user_profile(db, user_id)
    return user_profile  # Simply return the dictionary received from the repository

def update_preference(db: Session, user_id: UUID, preference_data: dict) -> bool:
    """
    Updates the user's preference in their profile and returns the update success status.
    
    Args:
        db: Database session.
        user_id: The ID of the user.
        preference_data: The new preference data to be updated.
        
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return update_user_profile(db, user_id, preference_data)  