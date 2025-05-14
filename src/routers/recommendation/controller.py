from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .service import add_click_to_restaurant, get_recommendations, get_random_restaurants_details
from common_schemas.response import ApiResponse
from database import get_db
from uuid import UUID
from .model import AddClickRequest
from geopy.distance import geodesic

router = APIRouter()

@router.post("/add-click", response_model = ApiResponse, tags = ["Recommendation"])
def add_click(
    data: AddClickRequest,
    db: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint for adding a click from the current user to a specific restaurant.

    Args:
        data (AddClickRequest): The request body containing user_id and restaurant_id.
        db (Session): The database session for querying.

    Returns:
        ApiResponse: The result of the operation, containing status and message.
    """
    result = add_click_to_restaurant(db, data.user_id, data.restaurant_id)
    if result.status != 200:
        raise HTTPException(status_code=result.status, detail=result.message)
    
    return result

@router.get("/user/{user_uuid}", response_model=ApiResponse, tags=["Recommendation"])
async def get_recommendations_for_user(
    user_uuid: str, 
    top_n: int = 20, 
    user_lat: float = 10.768778567106164, 
    user_long: float = 106.74621772556752,
    session: Session = Depends(get_db)
) -> ApiResponse:
    """
    Get recommendations for a user based on their click history similar to top_n other users, using cosine similarity.
    
    Args:
        user_uuid (str): The user's UUID.
        top_n (int): The number of similar users to consider.
        user_lat (float): The user's latitude.
        user_long (float): The user's longitude.
        session (Session): The SQLAlchemy session object.

    Returns:
        ApiResponse: The response containing recommendations or error message.
    """
    user_uuid = UUID(user_uuid)
    try:
        recommendations = get_recommendations(user_uuid, top_n, session)
        if not recommendations:
            recommendations = get_random_restaurants_details(session, top_n)
        
        for rec in recommendations:
            rec.update({"distance": geodesic((rec.get("latitude", 0), rec.get("longitude", 0)), (user_lat, user_long)).km})

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
    
@router.get("/guest", response_model=ApiResponse, tags=["Recommendation"])
async def get_recommendations_for_guest(
    top_n: int = 8,
    user_lat: float = 10.768778567106164, 
    user_long: float = 106.74621772556752,
    session: Session = Depends(get_db)
) -> ApiResponse:
    """
    Endpoint to get 8 random restaurants and their details for a guest user.

    Args:
        top_n (int): The number of random restaurants to fetch (default is 8).
        user_lat (float): The user's latitude.
        user_long (float): The user's longitude.
        session (Session): The database session object.

    Returns:
        ApiResponse: A standardized response containing the restaurant details.
    """
    try:
        # Get random restaurant details from the service
        restaurants = get_random_restaurants_details(session, top_n)

        for rec in restaurants:
            rec.update({"distance": geodesic((rec.get("latitude", 0), rec.get("longitude", 0)), (user_lat, user_long)).km})

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
        raise HTTPException(status_code=500, detail=f"Failed to get random restaurants")