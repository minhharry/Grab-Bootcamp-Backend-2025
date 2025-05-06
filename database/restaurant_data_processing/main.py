from config.minio_config import init_minio_client
from config.spark_config import init_spark
from config.postgres_config import get_postgres_config
from data_processing.shopee_processing import process_shopee_data
from data_processing.googlemaps_processing import process_google_data
from data_processing.unified_processing import unify_data
from load_to_database.writer import write_to_postgres
from load_to_database.download_processed import download_processed_data
from load_to_database.download_processed import save_images_tables_as_csv

def main():
    # Khởi tạo MinIO
    client, minio_bucket = init_minio_client()

    # Khởi tạo Spark
    spark = init_spark()

    # Đường dẫn dữ liệu
    shopee_path = "s3a://grab-project-data/raw/shopeefood/data-shopee-food.jsonl"
    google_path = "s3a://grab-project-data/raw/googlemaps/googlemaps-restaurants-with-locations.jsonl"

    # Xử lý dữ liệu
    df_shopee = process_shopee_data(spark, shopee_path)
    df_google = process_google_data(spark, google_path)
    df_unified = unify_data(df_shopee, df_google)

    # Ghi vào PostgreSQL
    # postgres_config = get_postgres_config()
    # write_to_postgres(df_unified, postgres_config)
    
    download_processed_data(client, minio_bucket, df_unified)
    
    save_images_tables_as_csv(df_unified, "images_table_data/images.csv")

    spark.stop()

if __name__ == "__main__":
    main()