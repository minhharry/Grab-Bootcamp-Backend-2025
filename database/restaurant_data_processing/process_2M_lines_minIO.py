import time
import boto3
import io
import tempfile
import os
from pyspark.sql import SparkSession
from schemas.shopeefood_raw_schema import shopeefood_raw_schema
from data_processing.shopee_processing import process_shopee_data
from config.postgres_config import get_postgres_config
from load_data.write_from_spark_to_postgres import write_to_postgres
import logging
from config.spark_config import init_spark


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo client S3 cho MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id=os.get_env('MINIO_ROOT_USER'),
    aws_secret_access_key=os.get_env('MINIO_ROOT_PASSWORD'),
    region_name='us-east-1',
    config=boto3.session.Config(
        signature_version='s3v4',
        connect_timeout=120,  # 120 giây
        read_timeout=120,     # 120 giây
        retries={'max_attempts': 5, 'mode': 'standard'}
    )
)

def read_large_jsonl_in_chunks(bucket, key, chunk_size=10000):
    obj = s3.get_object(Bucket=bucket, Key=key)
    lines = obj['Body'].iter_lines()

    buffer = []
    for i, line in enumerate(lines, 1):
        buffer.append(line)
        if i % chunk_size == 0:
            yield b'\n'.join(buffer)
            buffer = []
    if buffer:
        yield b'\n'.join(buffer)

def process_chunk(spark, bucket, key, chunk_size=10000):
    temp_dir = tempfile.mkdtemp()
    postgres_config = get_postgres_config()
    
    for i, chunk in enumerate(read_large_jsonl_in_chunks(bucket, key, chunk_size)):
        # Lưu chunk vào file tạm
        temp_file = f"{temp_dir}/chunk_{i}.json"
        with open(temp_file, "wb") as f:
            f.write(chunk)
        
        # Đọc chunk vào Spark DataFrame
        df = spark.read.schema(shopeefood_raw_schema).json(temp_file)
        record_count = df.count()
        if record_count == 0:
            print(f"Chunk {i} is empty, skipping")
            os.remove(temp_file)
            continue
        
        print(f"Processing chunk {i} with {record_count} records")
        
        # Xử lý dữ liệu
        processed_df = process_shopee_data(spark, df)
        
        # Ghi vào PostgreSQL
        # print(f"Writing chunk {i} to PostgreSQL")
        write_to_postgres(processed_df, postgres_config)
        # print(f"Write chunk {i} to PostgreSQL done")
        
        # Dọn dẹp
        processed_df.unpersist()
        df.unpersist()
        os.remove(temp_file)
        # print(f"Cleaned up chunk {i}")
    
    print(f"Completed processing {key}")
    os.rmdir(temp_dir)

def main():
    spark = init_spark()
    bucket_name = "grab-project-data"
    date_str = "2025-05-01"
    files = [
        "raw/shopeefood/2025-05-01/shopeefood_20250501_001_2000000_lines.json"
    ]
    
    start_time = time.time()
    try:
        for key in files:
            process_chunk(spark, bucket_name, key, chunk_size=250)
    except Exception as e:
        print(f"Error processing file {key}: {e}")
        raise
    finally:
        end_time = time.time()  # Kết thúc đo thời gian
        elapsed_time = end_time - start_time
        print(f"Total time taken: {elapsed_time:.2f} seconds")
    
    spark.stop()

if __name__ == "__main__":
    main()