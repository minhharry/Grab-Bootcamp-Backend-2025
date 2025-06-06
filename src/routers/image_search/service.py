import torch
from PIL import Image
from io import BytesIO
from qdrant_client import QdrantClient
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import List
from .model import ImageResultItem
from model_loader import ml_models
from .repository import get_image_restaurant_data
from geopy.distance import geodesic

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = QdrantClient(host="localhost", port=6333)

async def search_similar_images(
    image_bytes: bytes,
    db: Session,
    top_n: int = 5,
    user_lat: float = 10.768778567106164,
    user_long: float = 106.74621772556752,
    collection_name: str = "images_embedding",
    limit: int = 100
) -> List[ImageResultItem]:
    """
    Searches for similar images based on the provided image bytes using a model and a Qdrant database.

    Args:
        image_bytes (bytes): The byte data of the image to search for.
        db (Session): The database session to interact with the database.
        top_n: The maximum number of restaurant to return
        collection_name (str): The name of the Qdrant collection to search in.
        limit (int): The maximum number of similar images to search.

    Returns:
        List[ImageResult]: A list of `ImageResult` models containing image and restaurant data.
    """
    # Load model, device, and preprocessing
    model = ml_models.get("model")
    device = ml_models.get("device")
    preprocess = ml_models.get("preprocess")

    # Prepare image
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    # Get embedding from the model
    with torch.no_grad():
        if device.type == "cuda":
            with torch.amp.autocast("cuda"):
                embedding = model.encode_image(image_tensor)
        else:
            embedding = model.encode_image(image_tensor)

    # Normalize the embedding
    embedding /= embedding.norm(dim=-1, keepdim=True)
    embedding = embedding.squeeze().cpu().numpy()

    # Search the Qdrant database for similar images
    search_result = client.search(
        collection_name=collection_name,
        query_vector=embedding.tolist(),
        with_payload=True,
        limit=limit,
    )

    # Get image restaurant data from the repository
    img_ids = [str(r.id) for r in search_result]

    data_map = get_image_restaurant_data(db, img_ids)
    # Create result list with data from the search and database
    results = []
    seen_restaurant_ids = set()
    for r in search_result:
        img_id = str(r.id)
        data = data_map.get(img_id)

        if data:
            restaurant_id = data.get("restaurant_id")
            if restaurant_id not in seen_restaurant_ids:
                seen_restaurant_ids.add(restaurant_id)
                result = ImageResultItem(score=r.score, **data)
                result.distance = geodesic((data.get("latitude", 0), data.get("longitude", 0)), (user_lat, user_long)).km
                results.append(result)

    results.sort(key=lambda x: x.score, reverse=True)
    results = [r for r in results if r.distance <= 20]
    return results[:top_n]
