from pyspark.sql import SparkSession
from pyspark.sql.functions import when, size, array, flatten, col, lit, udf, to_timestamp, concat_ws, transform, struct, explode, to_json
from pyspark.sql.types import StringType, FloatType, IntegerType, StructType, StructField, ArrayType
from pyspark.sql.functions import regexp_extract
from pyspark.sql.functions import expr
from uuid import uuid4
from utils.format_price_range import parse_price_range_str
from minio import Minio
# from dotenv import load_dotenv
import os
# load_dotenv()

client = Minio(
    "minio:9000",
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    # access_key="admin",
    # secret_key="12345678",
    region="ap-southeast-1",
    secure=False
)

minio_bucket = "grab-project-data"

found = client.bucket_exists(minio_bucket)
if not found:
    client.make_bucket(minio_bucket)

builder = SparkSession.builder \
    .appName("RestaurantDataProcessing") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("ipc.maximum.data.length", "100000000")
    
spark = builder.getOrCreate()

sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("MINIO_ROOT_USER"))
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("MINIO_ROOT_PASSWORD"))
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint.region", "ap-southeast-1")

# @udf(StringType())
# def uuid_gen():
#     return str(uuid4())

schema = StructType([
    StructField("price_min", FloatType(), True),
    StructField("price_max", FloatType(), True)
])

parse_price_range_udf = udf(parse_price_range_str, schema)

try:
    files = spark.sparkContext._jvm.org.apache.hadoop.fs.FileSystem.get(
        spark.sparkContext._jsc.hadoopConfiguration()
    ).listStatus(spark.sparkContext._jvm.org.apache.hadoop.fs.Path("s3a://grab-project-data/raw/shopee_food/"))
    for f in files:
        print(f.getPath().toString())
except Exception as e:
    print("Error accessing S3:", str(e))

shopee_path = "s3a://grab-project-data/raw/shopeefood/data-shopee-food.jsonl"
google_path = "s3a://grab-project-data/raw/googlemaps/quan_an_tp_hcm_google_maps_selenium.jsonl"

df_shopee = spark.read.json(shopee_path)
df_google = spark.read.json(google_path)

# df_google.show(10, truncate=False)

df_shopee_normalized = df_shopee.select(
    # uuid_gen().alias("restaurant_id"),
    expr("uuid()").alias("restaurant_id"),
    col("name").alias("restaurant_name"),
    col("avatar_url"),
    col("restaurant_type").alias("restaurant_description"),
    col("opening_hours"),
    to_json(parse_price_range_udf(col("price_range"))).alias("price_range"),
    col("address"),
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
            # uuid_gen().alias("review_id")
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
            # uuid_gen().alias("img_id")
            expr("uuid()").alias("img_id")
        )
    )
)
    

df_google_normalized = df_google.select(
    # uuid_gen().alias("restaurant_id"),
    expr("uuid()").alias("restaurant_id"),
    col("name").alias("restaurant_name"),
    col("avatar_url"),
    col("restaurant_type").alias("restaurant_description"),
    col("closing_time").alias("opening_hours"),
    to_json(parse_price_range_udf(col("price_range"))).alias("price_range"),
    col("address"),
    lit("GoogleMaps").alias("source"),
    col("restaurant_rating").cast("float").alias("restaurant_rating"),
    col("restaurant_rating_count").cast("int").alias("restaurant_rating_count"),
    col("reviews").alias("reviews"),
    flatten(col("reviews.photos")).alias("images"),
    lit(None).cast("string").alias("restaurant_url"),
    to_timestamp(col("crawl_time")).alias("crawl_time"),
    lit(None).cast("string").alias("crawl_id")
).withColumn(
    "reviews",
    transform(
        col("reviews"),
        lambda x: struct(
            # parse_user_rating(x["rating"]).alias("user_rating"),
            x.review_author.alias("review_author"),
            x.review_date.alias("review_date"),
            regexp_extract(x["rating"], r"(\d+(\.\d+)?)", 1).cast("float").alias("user_rating"),
            x["text"].alias("user_review"),
            # uuid_gen().alias("review_id")
            expr("uuid()").alias("review_id")
        )
    )
).withColumn(
    "images",
    when(col("images").isNotNull() & (size(col("images")) > 0),
         transform(
             col("images"),
             lambda x: struct(
                 lit(None).alias("food_name"),
                 lit(None).alias("food_price"),
                 x.alias("img_url"),
                #  uuid_gen().alias("img_id")
                expr("uuid()").alias("img_id")
             )
         )).otherwise(array().cast("array<struct<food_name:string,food_price:string,img_url:string,img_id:string>>"))
)

df_unified = df_shopee_normalized.unionByName(df_google_normalized, allowMissingColumns=True)

# Thông số kết nối PostgreSQL
postgres_url = "jdbc:postgresql://db:5432/restaurants"
postgres_properties = {
    "user": "postgres",
    "password": "example",
    "driver": "org.postgresql.Driver",
    "stringtype": "unspecified" # https://medium.com/@suffyan.asad1/writing-to-databases-using-jdbc-in-apache-spark-9a0eb2ce1a
}

# Trích xuất và ghi bảng restaurants
df_restaurants = df_unified.select(
    "restaurant_id",
    "restaurant_name",
    "avatar_url",
    "restaurant_description",
    "opening_hours",
    "price_range",
    "address",
    "source",
    "restaurant_rating",
    "restaurant_rating_count",
    "restaurant_url",
    "crawl_time",
    "crawl_id"
)

try:
    
    df_restaurants.write.jdbc(
        url=postgres_url,
        table= "restaurants",
        properties=postgres_properties,
        mode="append"
    )
    
except Exception as e:
    print(f"Lỗi khi ghi vào bảng restaurants: {e}")
    spark.stop()
    exit(1)

# Trích xuất và ghi bảng reviews
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

try:
    df_reviews.write.jdbc(
        url=postgres_url,
        table= "reviews",
        properties=postgres_properties,
        mode="append"
    )
except Exception as e:
    print(f"Lỗi khi ghi vào bảng reviews: {e}")
    spark.stop()
    exit(1)

# Trích xuất và ghi bảng images
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

try:
    df_images.write.jdbc(
        url=postgres_url,
        table= "images",
        properties=postgres_properties,
        mode="append"
    )
except Exception as e:
    print(f"Lỗi khi ghi vào bảng images: {e}")
    spark.stop()
    exit(1)

# Dừng Spark session
spark.stop()