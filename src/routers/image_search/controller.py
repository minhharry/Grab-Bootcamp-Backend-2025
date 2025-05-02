from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from .service import search_similar_images
from common_schemas.response import ApiResponse
from database import get_db

router = APIRouter()

@router.post("/search-image", response_model=ApiResponse)
async def search_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to search for similar images using a given image file.
    Validates the file type, reads the file content, and searches for similar images.

    Args:
        file (UploadFile): The image file uploaded by the user.
        db (Session): Database session for interacting with the DB.

    Returns:
        ApiResponse: Search results, including image similarity data and metadata.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File isn't an image")

    # Read the image file
    image_bytes = await file.read()

    # Fetch search results using the service layer
    results = await search_similar_images(image_bytes, db)
    
    if not results:
        raise HTTPException(status_code=404, detail="No similar images found")

    # Return the response with data and metadata
    return ApiResponse(
        status=200,
        message="Data retrieved successfully",
        data=results,  # List of SearchResult models
        metadata=None  # No pagination, as this is a direct search response
    )
