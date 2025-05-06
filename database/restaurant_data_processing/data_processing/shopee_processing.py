from pyspark.sql.functions import expr, col, lit, to_timestamp, concat_ws, transform, struct, to_json
from udfs.price_range_udf import parse_price_range_udf

def process_shopee_data(spark, shopee_path):
    df_shopee = spark.read.json(shopee_path)
    df_shopee_normalized = df_shopee.select(
        expr("uuid()").alias("restaurant_id"),
        col("name").alias("restaurant_name"),
        col("avatar_url"),
        col("restaurant_type").alias("restaurant_description"),
        col("opening_hours"),
        to_json(parse_price_range_udf(col("price_range"))).alias("price_range"),
        col("address"),
        col("longitude"),
        col("latitude"),
        lit("ShopeeFood").alias("source"),
        (col("avgRating").cast("float") / 2).alias("restaurant_rating"),
        col("rating_count").cast("int").alias("restaurant_rating_count"),
        col("reviews").alias("reviews"),
        col("images").alias("images"),
        col("restaurant_url"),
        to_timestamp(col("crawl_time")).alias("crawl_time"),
        col("crawl_id")
    ).withColumn(
        "reviews",
        transform(
            col("reviews"),
            lambda x: struct(
                x.Author.alias("review_author"),
                x.Review_date.alias("review_date"),
                (x.AvgRating.cast("float") / 2).alias("user_rating"),
                concat_ws(", ", x["Title"], x["Description"]).alias("user_review"),
                expr("uuid()").alias("review_id")
            )
        )
    ).withColumn(
        "images",
        transform(
            col("images"),
            lambda x: struct(
                x['name'].alias("food_name"),
                x.current_price.alias("food_price"),
                x.img_url.alias("img_url"),
                expr("uuid()").alias("img_id")
            )
        )
    )
    return df_shopee_normalized