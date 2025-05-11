from pyspark.sql.functions import array, size, when, sha2, expr, col, lit, to_timestamp, concat_ws, transform, struct, to_json
from udfs.price_range_udf import parse_price_range_udf

def process_shopee_data(spark, shopee_path):
    # df_shopee = spark.read.json(shopee_path)
    df_shopee_normalized = shopee_path.select(
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
        col("crawl_id"),
        sha2(
            concat_ws(
                "|",
                col("name"),
                col("address")
            ),
            256
        ).alias("restaurant_hash")
    ).withColumn(
        "reviews",
        when( col("reviews").isNotNull() & (size(col("reviews")) > 0),
        transform(
            col("reviews"),
            lambda x: struct(
                x.Author.alias("review_author"),
                x.Review_date.alias("review_date"),
                (x.AvgRating.cast("float") / 2).alias("user_rating"),
                concat_ws(", ", x["Title"], x["Description"]).alias("user_review"),
                sha2(
                    concat_ws(
                        "|",
                        x.Author,
                        x.AvgRating,
                        concat_ws(", ", x["Title"], x["Description"])
                    ),
                    256
                ).alias("review_hash"),
                expr("uuid()").alias("review_id")
            )
        )).otherwise(array().cast("array<struct<review_author:string,review_date:string,user_rating:float,user_review:string,review_hash:string,review_id:string>>"))
    ).withColumn(
        "images",
        when(col("images").isNotNull() & (size(col("images")) > 0),
        transform(
            col("images"),
            lambda x: struct(
                x['name'].alias("food_name"),
                x.current_price.alias("food_price"),
                x.img_url.alias("img_url"),
                sha2(
                    concat_ws(
                        "|",
                        x["name"],
                        x["img_url"]
                    ),
                    256
                ).alias("img_hash"),
                expr("uuid()").alias("img_id")
            )
        )).otherwise(array().cast("array<struct<food_name:string,food_price:string,img_url:string,img_hash:string,img_id:string>>"))
    )
    return df_shopee_normalized