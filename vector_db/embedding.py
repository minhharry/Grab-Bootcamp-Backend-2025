# Or you can generate image embeddings yourself using our Kaggle notebook:
#  👉 [Open the Kaggle Notebook](https://www.kaggle.com/code/colabnguyen/recognize-food-name-and-embedding)

import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import torch
import open_clip
from sqlalchemy.orm import Session
from vector_db.database import SessionLocal
from .model import ImageModel
from tqdm import tqdm
import json

device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms('ViT-H-14-378-quickgelu', pretrained='dfn5b')
model.to(device)
model.eval()

db: Session = SessionLocal()
images = db.query(ImageModel).filter(ImageModel.img_url != None).all()

rows = []

for img in tqdm(images):
    try:
        response = requests.get(img.img_url, timeout=10)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            features = model.encode_image(image_tensor)
            features /= features.norm(dim=-1, keepdim=True)
            vector = features.cpu().numpy().tolist()[0]
        
        rows.append({
            "image_id": str(img.img_id),
            "img_url": img.img_url,
            "vector": json.dumps(vector)  
        })

    except Exception as e:
        print(f"[ERROR] Skipping image {img.img_url}: {e}")

df = pd.DataFrame(rows)
df.to_csv("vector_db/image_vectors.csv", index=False)

print("CSV đã được tạo: image_vectors.csv")
