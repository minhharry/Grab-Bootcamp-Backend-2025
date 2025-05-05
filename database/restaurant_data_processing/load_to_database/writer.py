from pyspark.sql.functions import col, explode

def write_to_postgres(df_unified, postgres_config):
    try:
        # Ghi bảng restaurants
        df_restaurants = df_unified.select(
            "restaurant_id", "restaurant_name", "avatar_url", "restaurant_description",
            "opening_hours", "price_range", "address", "longitude", "latitude",
            "source", "restaurant_rating", "restaurant_rating_count", "restaurant_url",
            "crawl_time", "crawl_id"
        )
        df_restaurants.write.jdbc(
            url=postgres_config["url"],
            table="restaurants",
            properties=postgres_config["properties"],
            mode="append"
        )

        # Ghi bảng reviews
        df_reviews = df_unified.select(
            col("restaurant_id"),
            explode("reviews").alias("review")
        ).select(
            col("review.review_id").alias("review_id"),
            col("restaurant_id"),
            col("review.user_rating").alias("user_rating"),
            col("review.user_review").alias("user_review"),
            col("review.review_author").alias("review_user_name"),
            col("review.review_date").alias("review_date")
        )
        df_reviews.write.jdbc(
            url=postgres_config["url"],
            table="reviews",
            properties=postgres_config["properties"],
            mode="append"
        )

        # Ghi bảng images
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
        df_images.write.jdbc(
            url=postgres_config["url"],
            table="images",
            properties=postgres_config["properties"],
            mode="append"
        )
    except Exception as e:
        print(f"Lỗi khi ghi dữ liệu vào PostgreSQL: {e}")
        raise