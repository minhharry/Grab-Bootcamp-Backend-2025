from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .service import get_profile, update_preference
from .model import UserPreferenceUpdate
from database import get_db
from common_schemas.response import ApiResponse
router = APIRouter()

@router.get("/profile/{user_id}", response_model=ApiResponse)
def get_user_profile(user_id: UUID, db: Session = Depends(get_db)):
    """
    API to fetch the user profile and return it in ApiResponse format.
    
    Args:
        user_id: The ID of the user.
        db: Database session.
    
    Returns:
        ApiResponse: Contains the user profile data or error message if user is not found.
    """
    user_profile = get_profile(db, user_id)
    
    if not user_profile:
        return ApiResponse(
            status=404,
            message="User profile not found"
        )  # Return ApiResponse with user not found message
    
    return ApiResponse(
        status=200,
        message="User profile retrieved successfully",
        data=user_profile,
        metadata=None
    )  # Return the profile data wrapped in ApiResponse

@router.put("/profile/{user_id}/preference", response_model=ApiResponse)
def update_user_preference(user_id: UUID, preference: UserPreferenceUpdate, db: Session = Depends(get_db)):
    """
    API to update the user's preference in their profile.
    
    Args:
        user_id: The ID of the user.
        preference: The preference data to update.
        db: Database session.
    
    Returns:
        ApiResponse: The response model containing the update status.
    """
    preference_data = preference.model_dump()
    success = update_preference(db, user_id, preference_data)
    
    if not success:
        return ApiResponse(
            status=404,
            message="User profile not found or not updated"
        )  # Return ApiResponse if update fails (user not found)
    
    return ApiResponse(
        status=200,
        message="User profile updated successfully"
    )