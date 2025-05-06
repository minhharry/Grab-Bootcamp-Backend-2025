from minio import Minio
import os

def init_minio_client():
    client = Minio(
        "minio:9000",
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        region="ap-southeast-1",
        secure=False
    )
    minio_bucket = "grab-project-data"
    if not client.bucket_exists(minio_bucket):
        client.make_bucket(minio_bucket)
    return client, minio_bucket