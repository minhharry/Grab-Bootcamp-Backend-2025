
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from .service import search_similar_images
from .model import SearchResponse
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.post("/search-image", response_model=SearchResponse)
async def search_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File isn't an image")

    image_bytes = await file.read()
    results = await search_similar_images(image_bytes, db)
    return {"results": results}
