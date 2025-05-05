from pyspark.sql.types import StructType, StructField, FloatType

price_range_schema = StructType([
    StructField("price_min", FloatType(), True),
    StructField("price_max", FloatType(), True)
])