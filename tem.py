from pyspark.sql import SparkSession
from schemas.shopeefood_raw_schema import shopeefood_raw_schema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_spark():
    return SparkSession.builder \
        .appName("ConvertJSONLtoParquet") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "12345678") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.sql.files.maxPartitionBytes", "512k") \
        .getOrCreate()

def convert_jsonl_to_parquet(spark, input_path, output_path, num_partitions):
    df = spark.read.schema(shopeefood_raw_schema).json(input_path)
    total_rows = df.count()
    logger.info(f"Converting {input_path} with {total_rows} rows to Parquet")
    # Chia thành num_partitions, mỗi partition ~7 dòng
    df.repartition(num_partitions).write.mode("overwrite").parquet(output_path)
    logger.info(f"Saved Parquet to {output_path} with {num_partitions} partitions")

def main():
    spark = init_spark()
    bucket_name = "grab-project-data"
    date_str = "2025-05-08"
    files = [
        ("shopeefood_20250508_001.json", 2),  # 8 dòng -> 2 partitions (~4 dòng mỗi partition)
        ("shopeefood_20250508_002.json", 4)   # 28 dòng -> 4 partitions (~7 dòng mỗi partition)
    ]
    
    for file, num_partitions in files:
        input_path = f"s3a://{bucket_name}/raw/shopeefood/{date_str}/{file}"
        output_path = f"s3a://{bucket_name}/raw/shopeefood/{date_str}/{file.split('.json')[0]}_parquet"
        convert_jsonl_to_parquet(spark, input_path, output_path, num_partitions)
    
    spark.stop()

if __name__ == "__main__":
    main()