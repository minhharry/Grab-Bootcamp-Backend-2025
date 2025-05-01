from minio import Minio
from dotenv import load_dotenv
import os
load_dotenv()

print("Start uploading data to MinIO")

client = Minio(
    "localhost:9000",
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    region="ap-southeast-1",
    secure=False
)

print("Connected to MinIO")

bucket_name = "grab-project-data"

found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)

script_dir = os.path.dirname(os.path.abspath(__file__))

data_sources = ["shopeefood", "googlemaps"]
for source in data_sources:
    folder_path = os.path.join(script_dir, "raw-data", source)
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for name in file_names:
        source_file = os.path.join(folder_path, name)
        destination_file = os.path.join("raw", source, name)
        client.fput_object(bucket_name, destination_file, source_file)
        print(f"Đã upload: {destination_file}")