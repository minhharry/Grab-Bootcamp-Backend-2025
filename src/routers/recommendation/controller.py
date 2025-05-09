from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .service import add_click_to_restaurant, get_recommendations, get_random_restaurants_details
from common_schemas.response import ApiResponse
from database import get_db
from uuid import UUID


router = APIRouter()

@router.post("/add-click", response_model=ApiResponse)
def add_click(
    user_id: UUID,
    restaurant_id: UUID,
    db: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint for adding a click from the current user to a specific restaurant.

    Args:
        token (str): The JWT token passed in the Authorization header.
        restaurant_id (UUID): The restaurant's ID
        db (Session): The database session for querying

    Returns:
        ApiResponse: The result of the operation, containing status and message.
    """

    result = add_click_to_restaurant(db, user_id, restaurant_id)
    if result.status != 200:
        raise HTTPException(status_code=result.status, detail=result.message)
    
    return result

@router.get("/{user_uuid}", response_model=ApiResponse)
async def get_recommendations_for_user(
    user_uuid: str, 
    top_n: int = 20, 
    session: Session = Depends(get_db)
) -> ApiResponse:
    """
    Get recommendations for a user based on their click history similar to top_n other users, using cosine similarity.
    
    Args:
        user_uuid (str): The user's UUID.
        top_n (int): The number of similar users to consider.
        session (Session): The SQLAlchemy session object.

    Returns:
        ApiResponse: The response containing recommendations or error message.
    """
    user_uuid = UUID(user_uuid)
    try:
        recommendations = get_recommendations(user_uuid, top_n, session)
        print(recommendations)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found")
        
        return ApiResponse(
            status=200,
            message="Data retrieved successfully",
            data=recommendations,
            metadata=None
        )
    
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to get recommendations")
    
@router.get("/", response_model=ApiResponse)
async def get_recommendations_for_guest(
    top_n: int = 8,
    session: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint to get 10 random restaurants and their details for a guest user.

    Args:
        top_n (int): The number of random restaurants to fetch (default is 20).
        session (Session): The database session object.

    Returns:
        ApiResponse: A standardized response containing the restaurant details.
    """
    try:
        # Get random restaurant details from the service
        restaurants = get_random_restaurants_details(session, top_n)

        if not restaurants:
            raise HTTPException(status_code=404, detail="No restaurants found")

        # Return the response with data and metadata
        return ApiResponse(
            status=200,
            message="Random restaurants retrieved successfully",
            data=restaurants,
            metadata=None
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to get random restaurants{e}")
