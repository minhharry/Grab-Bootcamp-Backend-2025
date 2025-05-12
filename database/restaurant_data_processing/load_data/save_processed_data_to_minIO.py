import os
from pyspark.sql.functions import col, explode

def save_processed_data_to_minIO(spark, bucket_name, df_unified):
    output_path = f"s3a://{bucket_name}/processed/restaurants_unified/"
    
    df_unified.write \
        .format("json") \
        .mode("append") \
        .save(f"{output_path}")
        