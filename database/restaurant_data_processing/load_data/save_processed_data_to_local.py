import os    

def save_processed_data_to_local(client, bucket_name, prefix, local_dir):
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