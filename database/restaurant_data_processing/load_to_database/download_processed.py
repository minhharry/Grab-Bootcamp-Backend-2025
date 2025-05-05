import os

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