import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import json

client = QdrantClient(host="localhost", port=6333)

df = pd.read_csv('vector_db/image_vectors.csv')

df['vector'] = df['vector'].apply(lambda x: json.loads(x)) 


collection_name = "images_embedding" 

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)



for index, row in df.iterrows():
    payload = {"url": row['img_url']}  
    vector = row['vector'] 
    restaurant_id = str(row['image_id']) 
    

    client.upsert(
        collection_name=collection_name,
        points=[{
            "id": restaurant_id,
            "vector": vector,
            "payload": payload
        }]
    )

print("Dữ liệu đã được đưa vào Qdrant.")
