
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CovidTransform").getOrCreate()
df = spark.read.csv("s3://your-bucket-name/raw/owid/owid-covid-data.csv", header=True, inferSchema=True)

# Example transformation
df = df.filter("passenger_count > 0")
df.write.parquet("s3://your-bucket-name/processed/", mode="overwrite")
