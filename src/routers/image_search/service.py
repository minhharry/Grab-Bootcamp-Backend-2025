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
from utils import haversine
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = QdrantClient(host="localhost", port=6333)

async def search_similar_images(
    image_bytes: bytes,
    db: Session,
    top_n: int = 5,
    user_location: dict = None,
    collection_name: str = "images_embedding",
    limit: int = 15
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
    """
    for r in search_result:
        img_id = str(r.id)
        data = data_map.get(img_id)

        if data:
            restaurant_id = data.get("restaurant_id")
            restaurant_location = (data.get("latitude"), data.get("longitude"))

            if user_location:
                user_coordinates = (user_location['latitude'], user_location['longitude'])
                distance = geodesic(user_coordinates, restaurant_location).kilometers
                distance_score = 1 / (distance + 0.0001) 
            else:
                distance_score = 0


            similarity_score = r.score
            final_score = 2/((1/similarity_score) + (1/distance_score))
            if restaurant_id not in seen_restaurant_ids:
                seen_restaurant_ids.add(restaurant_id)
                result = ImageResultItem(similar_score=r.score, final_score=final_score,**data)
                results.append(result)
    """
    top_results = sorted(search_result, key=lambda x: x.score, reverse=True)[:int(2/3*limit)]
    min_distance = float('inf')
    max_distance = float('-inf')

    # First, calculate 1/distance for each restaurant using geopy
    distances = []
    for r in top_results:
        restaurant_id = str(r.id)
        restaurant_data = data_map.get(restaurant_id)
        if restaurant_data:
            lat = restaurant_data.get("latitude")
            lon = restaurant_data.get("longitude")
            # Use geopy to calculate distance
            distance_km = haversine(
                user_location["latitude"], user_location["longitude"], lat, lon
            )  # Convert to kilometers
            if distance_km > 0:
                score = 1 / distance_km
                distances.append(score)
                min_distance = min(min_distance, score)
                max_distance = max(max_distance, score)

    for i, r in enumerate(top_results):
        restaurant_id = str(r.id)
        restaurant_data = data_map.get(restaurant_id)
        if restaurant_data:
            lat = restaurant_data.get("latitude")
            lon = restaurant_data.get("longitude")
            # Use geopy to calculate distance
            distance_km = haversine(
                user_location["latitude"], user_location["longitude"],
                lat, lon
            ) 
            if distance_km > 0:
                score = 1 / distance_km
                # Apply min-max scaling
                scaled_score = (score - min_distance) / (max_distance - min_distance) if max_distance != min_distance else 0
                # Calculate final score by averaging similarity score and distance score
                epsilon = 1e-6 
                #final_score = 2 / (1 / (r.score + epsilon) + 1 / (scaled_score + epsilon))
                final_score = r.score * 0.9 + scaled_score * 0.1
                # Add the result if the restaurant is not already in the seen_restaurant_ids set
                if restaurant_id not in seen_restaurant_ids:
                    seen_restaurant_ids.add(restaurant_id)
                    result = ImageResultItem(similar_score=r.score, final_score=final_score,**restaurant_data)
                    results.append(result)
    # Sort the results by score
    results.sort(key=lambda x: x.final_score, reverse=True)

    return results[:top_n]
