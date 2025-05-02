from sqlalchemy.orm import Session
from models import UserProfileModel
from uuid import UUID

def get_user_profile(db: Session, user_id: UUID) -> dict | None:
    """
    Fetches the user profile from the database using the user_id and returns it as a dictionary.
    
    Args:
        db: Database session.
        user_id: The ID of the user.
        
    Returns:
        dict: The user's profile data as a dictionary or None if not found.
    """
    user_profile = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()
    
    if not user_profile:
        return None
    
    return {
        "user_id": user_profile.user_id,
        "location": user_profile.location,
        "preference": user_profile.preference,
        "gender": user_profile.gender,
        "date_of_birth": user_profile.date_of_birth
    }

def update_user_profile(db: Session, user_id: UUID, profile_data: dict) -> bool:
    """
    Updates the user profile with the provided preference data.
    
    Args:
        db: Database session.
        user_id: The ID of the user.
        profile_data: The data to update the user profile with.
        
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    user_profile = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()
    
    if not user_profile:
        return False  # Return False if the user profile doesn't exist

    # Update the preference field with the provided data
    if "preference" in profile_data and profile_data["preference"] is not None:
        user_profile.preference = profile_data["preference"]

    db.commit()  # Commit the changes to the database
    db.refresh(user_profile)
    return True 