from pyspark.sql.functions import col, explode, lit
from retry import retry
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

@retry(tries=3, delay=2, backoff=2, exceptions=(Exception,))
def write_with_retry(df, url, table, properties, mode):
    df.coalesce(1).write.jdbc(
        url=url,
        table=table,
        properties=properties,
        mode=mode
    )

def write_to_postgres(df_unified, postgres_config):
    # Update JDBC properties with batch settings
    jdbc_properties = postgres_config["properties"].copy()
    jdbc_properties.update({
        "batchsize": "2000",  # Write 1000 rows per batch
        "reWriteBatchedInserts": "true"  # Optimize batch inserts
    })

    df_unified = df_unified.fillna({
        "restaurant_id": "unknown",
        "restaurant_name": "unknown",
        "address": "unknown",
        "source": "unknown",
        "crawl_time": "1970-01-01 00:00:00",
        "crawl_id": "unknown"
    })

    try:
        # print("Writing to restaurants table")
        df_restaurants = df_unified.select(
            "restaurant_id", "restaurant_name", "avatar_url", "restaurant_description",
            "address", "longitude", "latitude", "source", "opening_hours", "price_range",
            "restaurant_rating", "restaurant_rating_count", "restaurant_url", "crawl_time",
            "crawl_id"
        )
        # df_restaurants.printSchema()
        write_with_retry(
            df_restaurants,
            postgres_config["url"],
            "restaurants",
            jdbc_properties,
            "append"
        )
    except Exception as e:
        logger.error(f"Error writing to restaurants table: {e}")

    try:
        # print("Writing to reviews table")
        df_reviews = df_unified.select(
            col("restaurant_id"), explode("reviews").alias("review"),
            col("crawl_time"), col("crawl_id")
        ).select(
            col("review.review_id").alias("review_id"), col("restaurant_id"),
            col("review.user_rating").alias("user_rating"), col("review.user_review").alias("user_review"),
            col("review.review_author").alias("review_user_name"), col("review.review_date").alias("review_date"),
            col("crawl_time"), col("crawl_id")
        )
        # df_reviews.printSchema()
        write_with_retry(
            df_reviews,
            postgres_config["url"],
            "reviews",
            jdbc_properties,
            "append"
        )
    except Exception as e:
        logger.error(f"Error writing to reviews table: {e}")

    try:
        # print("Writing to images table")
        df_images = df_unified.select(
            col("restaurant_id"), explode("images").alias("image"),
            col("crawl_time"), col("crawl_id")
        ).select(
            col("image.img_id").alias("img_id"), col("restaurant_id"),
            col("image.food_name").alias("food_name"), col("image.food_price").alias("food_price"),
            col("image.img_url").alias("img_url"),
            col("crawl_time"), col("crawl_id")
        )
        # df_images.printSchema()
        write_with_retry(
            df_images,
            postgres_config["url"],
            "images",
            jdbc_properties,
            "append"
        )
        # print("Writing to images table completed")
    except Exception as e:
        logger.error(f"Error writing to images table: {e}")



# from pyspark.sql.functions import col, explode, lit
# from retry import retry

# @retry(tries=3, delay=2, backoff=2, exceptions=(Exception,))
# def write_with_retry(df, url, table, properties, mode):
#     df.coalesce(1).write.jdbc(url=url, table=table, properties=properties, mode=mode)

# def write_to_postgres(df_unified, postgres_config):
#     # Xử lý dữ liệu null
#     df_unified = df_unified.fillna({
#         "restaurant_id": "unknown",
#         "restaurant_name": "unknown",
#         "address": "unknown",
#         "source": "unknown",
#         "crawl_time": "1970-01-01 00:00:00",
#         "crawl_id": "unknown"
#     })

#     # Ghi bảng restaurants
#     try:
#         print("Schema of df_restaurants:")
#         df_restaurants = df_unified.select(
#             "restaurant_id", "restaurant_name", "avatar_url", "restaurant_description",
#             "address", "longitude", "latitude", "source", "opening_hours", "price_range",
#             "restaurant_rating", "restaurant_rating_count", "restaurant_url", "crawl_time",
#             "crawl_id"
#         )
#         df_restaurants.printSchema()
#         write_with_retry(
#             df_restaurants,
#             postgres_config["url"],
#             "restaurants",
#             postgres_config["properties"],
#             "append"
#         )
#     except Exception as e:
#         print(f"Error writing to restaurants table: {e}")

#     # Ghi bảng reviews
#     try:
#         print("Schema of df_reviews:")
#         df_reviews = df_unified.select(
#             col("restaurant_id"), explode("reviews").alias("review"),
#             col("crawl_time"), col("crawl_id")
#         ).select(
#             col("review.review_id").alias("review_id"), col("restaurant_id"),
#             col("review.user_rating").alias("user_rating"), col("review.user_review").alias("user_review"),
#             col("review.review_author").alias("review_user_name"), col("review.review_date").alias("review_date"),
#             col("crawl_time"), col("crawl_id")
#         )
#         df_reviews.printSchema()
#         write_with_retry(
#             df_reviews,
#             postgres_config["url"],
#             "reviews",
#             postgres_config["properties"],
#             "append"
#         )
#     except Exception as e:
#         print(f"Error writing to reviews table: {e}")

#     # Ghi bảng images
#     try:
#         print("Schema of df_images:")
#         df_images = df_unified.select(
#             col("restaurant_id"), explode("images").alias("image"),
#             col("crawl_time"), col("crawl_id")
#         ).select(
#             col("image.img_id").alias("img_id"), col("restaurant_id"),
#             col("image.food_name").alias("food_name"), col("image.food_price").alias("food_price"),
#             col("image.img_url").alias("img_url"),
#             col("crawl_time"), col("crawl_id")
#         )
#         df_images.printSchema()
#         write_with_retry(
#             df_images,
#             postgres_config["url"],
#             "images",
#             postgres_config["properties"],
#             "append"
#         )
#     except Exception as e:
#         print(f"Lỗi khi ghi dữ liệu vào PostgreSQL: {e}")
#         raise



# from pyspark.sql.functions import col, explode

# def write_to_postgres(df_unified, postgres_config):
#     try:
#         # Ghi bảng restaurants
#         df_restaurants = df_unified.select(
#             "restaurant_id", 
#             "restaurant_name", 
#             "avatar_url", 
#             "restaurant_description", 
#             "address", 
#             "longitude",
#             "latitude",
#             "source",
#             "opening_hours", 
#             "price_range", 
#             "restaurant_rating", 
#             "restaurant_rating_count",
#             "restaurant_url", 
#             "crawl_time", 
#             "crawl_id",
#             # "restaurant_hash"
#         )
#         df_restaurants.write.jdbc(
#             url=postgres_config["url"],
#             table="restaurants",
#             properties=postgres_config["properties"],
#             mode="append"
#         )

#         # Ghi bảng reviews
#         df_reviews = df_unified.select(
#             col("restaurant_id"),
#             explode("reviews").alias("review"),
#             col("crawl_time"),
#             col("crawl_id")
#         ).select(
#             col("review.review_id").alias("review_id"),
#             col("restaurant_id"),
#             col("review.user_rating").alias("user_rating"),
#             col("review.user_review").alias("user_review"),
#             col("review.review_author").alias("review_user_name"),
#             col("review.review_date").alias("review_date"),
#             # col("review.review_hash").alias("review_hash"),
#             col("crawl_time").alias("crawl_time"),
#             col("crawl_id").alias("crawl_id")
#         )
#         df_reviews.write.jdbc(
#             url=postgres_config["url"],
#             table="reviews",
#             properties=postgres_config["properties"],
#             mode="append"
#         )

#         # Ghi bảng images
#         df_images = df_unified.select(
#             col("restaurant_id"),
#             explode("images").alias("image"),
#             col("crawl_time"),
#             col("crawl_id")
#         ).select(
#             col("image.img_id").alias("img_id"),
#             col("restaurant_id"),
#             col("image.food_name").alias("food_name"),
#             col("image.food_price").alias("food_price"),
#             col("image.img_url").alias("img_url"),
#             # col("image.img_hash").alias("img_hash"),
#             col("crawl_time").alias("crawl_time"),
#             col("crawl_id").alias("crawl_id")
#         )
#         df_images.write.jdbc(
#             url=postgres_config["url"],
#             table="images",
#             properties=postgres_config["properties"],
#             mode="append"
#         )
#     except Exception as e:
#         print(f"Lỗi khi ghi dữ liệu vào PostgreSQL: {e}")
#         raise