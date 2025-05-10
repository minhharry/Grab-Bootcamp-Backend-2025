import os
from pyspark.sql.functions import col, explode

def save_processed_data_to_minIO(spark, bucket_name, df_unified):
    output_path = f"s3a://{bucket_name}/processed/output/restaurants_unified/"
    
    try:
        
        a = 1/0 # cố tình gây lỗi để vào exception
        
        df_old = spark.read.json(output_path)
        # Lấy danh sách hash từ dữ liệu cũ
        old_hashes = df_old.select("hash").distinct()
        
        
        # Tìm các bản ghi trùng lặp bằng inner join
        df_duplicates = df_unified.join(
            old_hashes,
            "hash",
            "inner"  # Lấy các bản ghi có hash trùng
        )
        
        # Đếm số bản ghi trùng lặp
        duplicate_count = df_duplicates.count()
        print(f"Số bản ghi trùng lặp: {duplicate_count}")
        
        # In một số bản ghi trùng lặp (nếu có)
        if duplicate_count > 0:
            print("Một số bản ghi trùng lặp (hiển thị tối đa 5 bản ghi):")
            df_duplicates.select(
                "restaurant_name", "address", "source", "hash"
            ).show(5, truncate=False)
        else:
            print("Không có bản ghi trùng lặp.")
        
        
        # Loại bỏ các bản ghi trong df_unified có hash trùng với dữ liệu cũ
        df_unified_deduped = df_unified.join(
            old_hashes,
            "hash",
            "left_anti"  # Chỉ giữ các bản ghi không có hash trùng
        )
        
        df_unified_deduped_count = df_unified_deduped.count()
        print(f"Số bản ghi không bị trùng: {df_unified_deduped_count}")
        
    except Exception as e:
        print(f"Không thể đọc dữ liệu cũ hoặc dữ liệu cũ không tồn tại: {e}")
        df_unified_deduped = df_unified
    
    df_unified_deduped.write \
        .format("json") \
        .mode("append") \
        .save(f"{output_path}")
        