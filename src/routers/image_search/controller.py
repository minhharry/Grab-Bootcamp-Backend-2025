import torch
import numpy as np
from PIL import Image
from io import BytesIO
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
import open_clip
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import List, Dict
from .model import ImageResult
from model_loader import model, preprocess, device

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("API_KEY")  
)

def fetch_image_restaurant_data(db: Session, img_ids: List[str]) -> Dict[str, dict]:
    query = text("""
        SELECT
            i.img_id, i.restaurant_id, i.food_name, i.food_price, i.img_url,
            r.restaurant_name, r.address, r.restaurant_rating, r.restaurant_url
        FROM images i
        LEFT JOIN restaurants r ON i.restaurant_id = r.restaurant_id
        WHERE i.img_id = ANY(ARRAY[:img_ids]::uuid[])
    """)
    rows = db.execute(query, {"img_ids": img_ids}).fetchall()
    return {str(row.img_id): dict(row._mapping) for row in rows}

async def search_similar_images(
    image_bytes: bytes,
    db: Session,
    collection_name: str = "food_image_embeddings",
    limit: int = 5
) -> List[ImageResult]:

    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        if device.type == "cuda":
            with torch.amp.autocast("cuda"):
                embedding = model.encode_image(image_tensor)
        else:
            embedding = model.encode_image(image_tensor)

    embedding /= embedding.norm(dim=-1, keepdim=True)
    embedding = embedding.squeeze().cpu().numpy()

    search_result = client.search(
        collection_name=collection_name,
        query_vector=embedding.tolist(),
        with_payload=True,
        limit=limit,
    )

    img_ids = [str(r.id) for r in search_result]
    data_map = fetch_image_restaurant_data(db, img_ids)

    results = []
    for r in search_result:
        img_id = str(r.id)
        data = data_map.get(img_id)

        if data:
            result = ImageResult(score=r.score, **data)
            results.append(result)

    results.sort(key=lambda x: x.score, reverse=True)
    return results