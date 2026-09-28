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

Spark generated a `part-*.csv` result file and a zero-byte `_SUCCESS` marker. The `_SUCCESS` file is normal Spark output metadata; it does not contain the CSV data.

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

## Commands

### AWS CLI Commands

#### 1. Install AWS CLI

Install AWS CLI v2:

```bash
curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
```

If `unzip` is missing:

```bash
sudo apt update
sudo apt install unzip -y
```

Verify AWS CLI:

```bash
aws --version
```

#### 2. Configure / Verify AWS Access

Check the active AWS identity:

```bash
aws sts get-caller-identity
```

#### 3. Create the S3 Bucket

```bash
aws s3 mb s3://cloud-fundamentals-sales-vishnupriya-2026 --region ap-south-1
```

List buckets:

```bash
aws s3 ls
```

#### 4. Upload sales.csv to S3

```bash
aws s3 cp sales.csv s3://cloud-fundamentals-sales-vishnupriya-2026/sales/sales.csv
```

Verify the uploaded file:

```bash
aws s3 ls s3://cloud-fundamentals-sales-vishnupriya-2026/sales/
```

#### 5. Check S3 Object

```bash
aws s3 ls s3://cloud-fundamentals-sales-vishnupriya-2026/sales/sales.csv
```

### Spark Commands

#### 6. Run Spark Locally

Go to the project directory:

```bash
cd ~/cloud-sales-lab
```

Run the Spark analysis:

```bash
spark-submit sales_analysis.py
```

#### 7. Check Spark Output

List generated files:

```bash
find output -maxdepth 2 -type f -print
```

Read the category result:

```bash
cat output/category_sales/part-*.csv
```

Expected category output:

```text
category,total_revenue
Electronics,5000
Clothing,1460
Furniture,2800
```

### Git Commands

#### 8. Git Commands Used

Go to the GitHub practice repository:

```bash
cd ~/AWS-Practice
```

Check repository status:

```bash
git status
```

Stage the practice:

```bash
git add aws-s3-sales-data-lake
```

Commit:

```bash
git commit -m "Add AWS S3 sales data lake and Spark practice"
```

Push:

```bash
git push origin main
```

Verify:

```bash
git status
```

Expected final status:

```text
nothing to commit, working tree clean
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
- **_SUCCESS** — Spark marker indicating a successful output write.

## Practice Structure

```
aws-s3-sales-data-lake/
├── README.md
├── .gitignore
├── sales.csv
├── sales_analysis.py
├── output/
│   └── category_sales/
│       ├── _SUCCESS
│       └── part-*.csv
├── screenshots/
└── notes/
```

## Screenshots

The `screenshots/` folder contains screenshots documenting the AWS CLI, S3, Spark processing, outputs, and final Git push.


## Execution Summary

| Step | Status |
|---|---|
| AWS CLI installed | ✅ |
| AWS identity verified | ✅ |
| S3 bucket created | ✅ |
| Dataset uploaded to S3 | ✅ |
| Spark application created | ✅ |
| Revenue calculated | ✅ |
| Category aggregation completed | ✅ |
| City aggregation completed | ✅ |
| Spark CSV output generated | ✅ |
| GitHub repository updated | ✅ |
| Screenshots added | ✅ |

## Prerequisites

Before running this practice, make sure the following are available:

- AWS account with CLI access
- AWS CLI v2
- Ubuntu / WSL2
- Java
- Apache Spark
- PySpark
- Python
- Git
- GitHub account

Verify the main tools:

```bash
aws --version
java -version
spark-submit --version
python3 --version
git --version
```

## Troubleshooting Notes

### AWS CLI: unzip missing

If the AWS CLI installation reports that `unzip` is missing:

```bash
sudo apt update
sudo apt install unzip -y
```

### Spark tries localhost:9000

For this local practice, the Spark application uses an explicit local file URI for the dataset and output. This prevents Spark from interpreting the path as an HDFS location.

### `_SUCCESS` is empty

This is expected. Spark creates `_SUCCESS` as a zero-byte success marker. The actual data is stored in the `part-*.csv` file.

### `.crc` files

Spark may create checksum files such as `.crc`. They are excluded from Git using `.gitignore` because they are generated metadata rather than project source files.

## Learning Outcome

This practice provides hands-on experience with:

- Cloud object storage using Amazon S3
- AWS CLI commands
- CSV data handling
- Spark DataFrames
- Derived columns
- Aggregation with `groupBy()` and `sum()`
- Sorting with `orderBy()`
- Spark CSV output
- Handling a cloud-service limitation with a local processing fallback
- Git version control and GitHub documentation

## Final Result

The complete practice contains the dataset, Spark source code, generated output, execution screenshots, and documentation in one GitHub practice folder.

## Result

The main S3 + Spark sales analysis and the optional city-revenue challenge were completed successfully.


## AWS Lambda Serverless Processing

As an alternative to the unavailable Amazon EMR service, AWS Lambda was added to this same S3 sales data lake practice.

The Lambda function processes the same `sales/sales.csv` file stored in the S3 bucket.

### Lambda Architecture

```text
sales.csv
   ↓
Amazon S3
sales/
   ↓ S3 ObjectCreated event
AWS Lambda
sales-data-lambda
   ↓
Revenue by category
   ↓
Amazon S3
output/lambda/category_sales.csv
```

### Lambda Configuration

Function:

```text
sales-data-lambda
```

Region:

```text
ap-south-1
```

Runtime:

```text
Python 3.14
```

S3 trigger:

- Event: All object create events
- Prefix: `sales/`
- Suffix: `.csv`

### Lambda Processing

The Lambda function:

1. Receives the S3 ObjectCreated event.
2. Reads `sales/sales.csv` from S3.
3. Calculates `quantity × price` for each row.
4. Aggregates revenue by category.
5. Writes the result to `output/lambda/category_sales.csv`.

### Lambda Output

```text
category,total_revenue
Clothing,1460
Electronics,5000
Furniture,2800
```

The Lambda output matches the category-level revenue produced by the Spark processing.

### Lambda IAM Permissions

The Lambda execution role includes:

- `AWSLambdaBasicExecutionRole`
- `s3:GetObject` for the `sales/*` input path
- `s3:PutObject` for the `output/lambda/*` output path

### Lambda Test

A test event named `s3-sales-test` was used to simulate an S3 ObjectCreated event for:

```text
sales/sales.csv
```

The Lambda test executed successfully.

### Lambda Files

The Lambda implementation and generated output are stored inside this same practice:

```text
aws-s3-sales-data-lake/
├── lambda_function.py
└── output/
    └── lambda/
        └── category_sales.csv
```
