from minio import Minio
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import global_config as config
load_dotenv()

def upload_to_minio(client, bucket_name, local_path, source, date_str):
    object_name = f"raw/{source}/{date_str}/{os.path.basename(local_path)}"
    
    # Kiểm tra xem file đã tồn tại trên MinIO chưa
    try:
        client.stat_object(bucket_name, object_name)
        print(f"File {object_name} đã tồn tại trên MinIO, bỏ qua upload.")
        return False
    except Exception:
        # Upload file
        client.fput_object(bucket_name, object_name, local_path)
        print(f"Uploaded {local_path} to s3a://{bucket_name}/{object_name}")
        return True

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
print("Found bucket:", found)
if not found:
    client.make_bucket(bucket_name)

print(f"Bucket {bucket_name} đã tồn tại hoặc đã được tạo thành công.")

script_dir = os.path.dirname(os.path.abspath(__file__))

print("Script directory:", script_dir)

date_str_array = config.SELLECT_CRAWL_DATE_ARRAY
for date_str in date_str_array:
    # Upload file ShopeeFood
    local_shopee_dir = f"{script_dir}/raw_data/shopeefood/{date_str}"

    if os.path.exists(local_shopee_dir):
        for filename in os.listdir(local_shopee_dir):
            local_path = os.path.join(local_shopee_dir, filename)
            upload_to_minio(client, bucket_name, local_path, "shopeefood", date_str)
    else:
        print(f"Directory {local_shopee_dir} does not exist.")


    # Upload file Google Maps
    local_google_dir = f"{script_dir}/raw_data/googlemaps/{date_str}"

    if os.path.exists(local_google_dir):
        for filename in os.listdir(local_google_dir):
            local_path = os.path.join(local_google_dir, filename)
            upload_to_minio(client, bucket_name, local_path, "googlemaps", date_str)
    else:
        print(f"Directory {local_google_dir} does not exist.")
