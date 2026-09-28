# AWS S3 Sales Data Lake & Spark Analysis

## Overview

This practice demonstrates a simple cloud data engineering workflow using Amazon S3 and Apache Spark.

The original lab architecture is:

```
sales.csv
   ↓
Amazon S3
   ↓
EMR / Spark
   ↓
Transformation
   ↓
Revenue Analysis
   ↓
Output
```

Because Amazon EMR was not available in the AWS account due to a subscription restriction, the Spark processing was completed locally with PySpark while the raw dataset was stored in Amazon S3.

## Objectives

- Create an AWS S3 bucket.
- Create a `sales/` data folder.
- Upload `sales.csv` to S3.
- Read and process the sales dataset with Spark.
- Calculate revenue using:

```
revenue = quantity × price
```

- Calculate revenue by category.
- Calculate revenue by city.
- Save the category aggregation as CSV output.
- Understand the roles of S3, EMR, Spark, EC2, and HDFS.

## AWS Resources

### S3 Bucket

```
cloud-fundamentals-sales-vishnupriya-2026
```

### Dataset location

```
s3://cloud-fundamentals-sales-vishnupriya-2026/sales/sales.csv
```

### Region

```
ap-south-1
```

## Dataset

The dataset contains:

- order_id
- order_date
- customer
- city
- category
- quantity
- price

The local copy is available as:

```
sales.csv
```

## Spark Processing

The Spark application is:

```
sales_analysis.py
```

The application:

1. Creates a Spark session.
2. Reads the CSV file.
3. Infers the schema.
4. Calculates revenue for every order.
5. Groups revenue by category.
6. Writes category results to CSV.
7. Groups revenue by city and sorts the results in descending order.

## Revenue by Category

The Spark result was:

| Category | Total Revenue |
|---|---:|
| Electronics | 5000 |
| Clothing | 1460 |
| Furniture | 2800 |

Output location:

```
output/category_sales/
```

Spark generated a `part-*.csv` file along with Spark's success/metadata files.

## Revenue by City

The optional challenge was also completed.

| City | Total Revenue |
|---|---:|
| Bangalore | 2760 |
| Hyderabad | 2500 |
| Pune | 2300 |
| Chennai | 1700 |

The results were sorted in descending order of total revenue.

## Important Spark Operations

### Create Revenue

```python
sales_df = df.withColumn(
    "revenue",
    col("quantity") * col("price")
)
```

### Revenue by Category

```python
category_sales = sales_df.groupBy("category") \
    .agg(
        sum("revenue").alias("total_revenue")
    )
```

### Revenue by City

```python
city_sales = sales_df.groupBy("city") \
    .agg(
        sum("revenue").alias("total_revenue")
    )

city_sales.orderBy(
    col("total_revenue").desc()
).show()
```

## Main Commands Used

### AWS CLI

Check AWS identity:

```bash
aws sts get-caller-identity
```

Create the S3 bucket:

```aws
aws s3 mb s3://cloud-fundamentals-sales-vishnupriya-2026 --region ap-south-1
```

Upload the dataset:

```bash
aws s3 cp sales.csv s3://cloud-fundamentals-sales-vishnupriya-2026/sales/sales.csv
```

Verify the upload:

```bash
aws s3 ls s3://cloud-fundamentals-sales-vishnupriya-2026/sales/
```

### Spark

Run the analysis:

```bash
spark-submit sales_analysis.py
```

Verify the generated output:

```bash
find output -maxdepth 2 -type f -print
```

Read the CSV result:

```bash
cat output/category_sales/part-*.csv
```

## EMR Note

An attempt was made to use Amazon EMR for the Big Data portion of the exercise. The AWS account returned a subscription-related restriction, so an EMR cluster could not be used.

The processing was therefore completed locally with Spark. This still demonstrates the Spark transformation and aggregation logic from the lab, while S3 remains the cloud storage component.

## Key Concepts Learned

- **Amazon S3** — object storage and data lake storage.
- **Amazon EC2** — virtual server / compute service.
- **Amazon EMR** — managed platform for Big Data frameworks such as Hadoop and Spark.
- **Apache Spark** — distributed data processing engine.
- **HDFS** — Hadoop Distributed File System.
- **groupBy()** — groups records by a column.
- **agg() / sum()** — performs aggregation.
- **orderBy()** — sorts the resulting data.
- **part-* files** — Spark commonly writes output as partitioned files.

## Practice Structure

```
aws-s3-sales-data-lake/
├── README.md
├── sales.csv
├── sales_analysis.py
├── output/
│   └── category_sales/
├── screenshots/
└── notes/
```

Screenshots and additional notes will be added to their respective folders.

## Result

The main S3 + Spark sales analysis and the optional city-revenue challenge were completed successfully.
