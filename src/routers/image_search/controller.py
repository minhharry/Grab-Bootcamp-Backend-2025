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

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, _, preprocess = open_clip.create_model_and_transforms("ViT-H-14-378-quickgelu", pretrained="dfn5b")
model.to(device)
model.eval()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("API_KEY")  
)

async def search_similar_images(
    image_bytes: bytes,
    db: Session,
    collection_name: str = "food_image_embeddings",
    limit: int = 5
):
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

    results = []
    for r in search_result:
        img_id = str(r.id)

        food_row = db.execute(text("""
            SELECT img_id, restaurant_id, food_name, food_price, img_url
            FROM images
            WHERE img_id = :img_id
        """), {"img_id": img_id}).fetchone()

        if food_row:
            food_data = dict(food_row._mapping)

            rest_data = {}
            if food_data.get("restaurant_id"):
                restaurant_row = db.execute(text("""
                    SELECT restaurant_name, address, restaurant_rating, restaurant_url
                    FROM restaurants
                    WHERE restaurant_id = :rest_id
                """), {"rest_id": food_data["restaurant_id"]}).fetchone()

                if restaurant_row:
                    rest_data = dict(restaurant_row._mapping)

            results.append({
                "score": r.score,
                **food_data,
                **rest_data
            })

    return results