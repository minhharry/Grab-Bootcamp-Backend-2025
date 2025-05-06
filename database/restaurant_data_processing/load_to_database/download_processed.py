import os
from pyspark.sql.functions import col, explode

def download_processed_data(client, bucket_name, df_unified):
    output_path = "s3a://grab-project-data/processed/output/restaurants_unified/"
    df_unified.write \
        .format("json") \
        .mode("overwrite") \
        .save(f"{output_path}/json")
        
    prefix = "processed/output/restaurants_unified/json/"
    local_dir = "processed_data/"

    if os.path.exists(local_dir):
        if os.path.isfile(local_dir):
            os.remove(local_dir)

    os.makedirs(local_dir, exist_ok=True)

    # Lấy danh sách object
    objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)

    for obj in objects:
        if obj.object_name.endswith(".json"):
            filename = os.path.basename(obj.object_name)
            local_path = os.path.join(local_dir, filename)
            client.fget_object(bucket_name, obj.object_name, local_path)
            print(f"Downloaded: {local_path}")
            
def save_images_tables_as_csv(df_unified, output_path):
    try:
        # Chuyển đổi và trích xuất dữ liệu hình ảnh
        df_images = df_unified.select(
            col("restaurant_id"),
            explode("images").alias("image")
        ).select(
            col("image.img_id").alias("img_id"),
            col("restaurant_id"),
            col("image.food_name").alias("food_name"),
            col("image.food_price").alias("food_price"),
            col("image.img_url").alias("img_url")
        )

        # Lưu DataFrame vào file CSV
        df_images.write \
            .mode("overwrite") \
            .option("header", "true") \
            .option("encoding", "UTF-8") \
            .csv(output_path)

        print(f"Đã lưu DataFrame vào {output_path}")
        return True

    except Exception as e:
        print(f"Lỗi khi lưu file CSV: {e}")
        return False