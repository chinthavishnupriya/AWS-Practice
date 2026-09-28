from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = SparkSession.builder \
    .appName("SalesAnalysis") \
    .getOrCreate()

# Read sales.csv
df = spark.read.csv(
    "file:///home/vishnupriya/cloud-sales-lab/sales.csv",
    header=True,
    inferSchema=True
)

print("=== Schema ===")
df.printSchema()

print("=== Original Data ===")
df.show()

# Calculate revenue = quantity * price
sales_df = df.withColumn(
    "revenue",
    col("quantity") * col("price")
)

print("=== Sales With Revenue ===")
sales_df.select(
    "order_id",
    "category",
    "quantity",
    "price",
    "revenue"
).show()

# Revenue by category
category_sales = sales_df.groupBy("category").agg(
    sum("revenue").alias("total_revenue")
)

print("=== Revenue By Category ===")
category_sales.show()

# Save result
category_sales.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("file:///home/vishnupriya/cloud-sales-lab/output/category_sales")
city_sales = sales_df.groupBy("city") \
    .agg(
        sum("revenue").alias("total_revenue")
    )

print("Revenue by City:")
city_sales.orderBy(
    col("total_revenue").desc()
).show()
spark.stop()
