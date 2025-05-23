from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from .service import search_similar_images
from common_schemas.response import ApiResponse
from database import get_db
from geopy.distance import geodesic
router = APIRouter()

@router.post("", response_model=ApiResponse, tags = ["Image Search"])
async def search_image(
    file: UploadFile = File(...), 
    top_n: int = 5, 
    user_lat: float = 10.768778567106164, 
    user_long: float = 106.74621772556752, 
    db: Session = Depends(get_db)
    )-> ApiResponse:
    """
    Endpoint to search for similar images using a given image file.
    Validates the file type, reads the file content, and searches for similar images.

    Args:
        file (UploadFile): The image file uploaded by the user.
        top_n: The maximum number of restaurant to return
        db (Session): Database session for interacting with the DB.

    Returns:
        ApiResponse: Search results, including image similarity data and metadata.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File isn't an image")

    image_bytes = await file.read()

    results = await search_similar_images(image_bytes, db, top_n, user_lat, user_long)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No similar images found"
        )

    # Return the response with data and metadata
    return ApiResponse(
        status=200,
        message="Data retrieved successfully",
        data=results,  # List of SearchResult models
        metadata=None  # No pagination, as this is a direct search response
    )
