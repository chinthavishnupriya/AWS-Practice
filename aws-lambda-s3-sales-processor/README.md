# AWS Lambda S3 Sales Processor

## Overview

This practice demonstrates how to use **AWS Lambda** with **Amazon S3** to process a sales CSV file automatically.

When `sales.csv` is uploaded to the S3 `sales/` folder, an S3 ObjectCreated event triggers the Lambda function. The Lambda function reads the CSV file, calculates total revenue by product category, and writes the result back to S3.

## Architecture

```text
sales.csv
    |
    v
Amazon S3
sales/
    |
    | ObjectCreated event
    v
AWS Lambda
sales-data-lambda
    |
    | Calculate revenue by category
    v
Amazon S3
output/lambda/category_sales.csv
```

## Objectives

- Create an AWS Lambda function using Python.
- Connect Amazon S3 with AWS Lambda.
- Trigger Lambda when a CSV file is uploaded to S3.
- Read sales data from S3.
- Calculate revenue using:
  `revenue = quantity × price`
- Aggregate revenue by product category.
- Write the processed result back to S3.
- Verify the Lambda output.

## AWS Resources

### S3 Bucket

```text
cloud-fundamentals-sales-vishnupriya-2026
```

Region: `ap-south-1`

Input:

```text
s3://cloud-fundamentals-sales-vishnupriya-2026/sales/sales.csv
```

Output:

```text
s3://cloud-fundamentals-sales-vishnupriya-2026/output/lambda/category_sales.csv
```

### Lambda Function

Function name: `sales-data-lambda`

Runtime: `Python 3.14`

Region: `ap-south-1`

## S3 Trigger Configuration

The Lambda function uses an S3 trigger with:

- Event type: All object create events
- Bucket: `cloud-fundamentals-sales-vishnupriya-2026`
- Prefix: `sales/`
- Suffix: `.csv`

## Lambda Processing

The Lambda function:

1. Receives the S3 event.
2. Extracts the bucket name and object key.
3. Reads the CSV file from S3.
4. Reads `quantity`, `price`, and `category`.
5. Calculates revenue for each row.
6. Aggregates revenue by category.
7. Creates an output CSV.
8. Uploads the result to `output/lambda/category_sales.csv`.

## IAM Permissions

The Lambda execution role has:

- `AWSLambdaBasicExecutionRole`
- Custom S3 permissions for reading the input and writing the output.

The custom permissions allow `s3:GetObject` on `sales/*` and `s3:PutObject` on `output/lambda/*`.

## Test Event

A Lambda test event named `s3-sales-test` was used to simulate an S3 ObjectCreated event for `sales/sales.csv`.

The Lambda test executed successfully.

## Output

The Lambda generated:

```text
category,total_revenue
Clothing,1460
Electronics,5000
Furniture,2800
```

Local output file:

```text
output/category_sales.csv
```

The Lambda result matches the category-level revenue calculated in the Spark sales-processing practice.

## Local Files

```text
aws-lambda-s3-sales-processor/
├── README.md
├── .gitignore
├── lambda_function.py
├── output/
│   └── category_sales.csv
└── screenshots/
```

## Verification

Python syntax was verified locally using:

```bash
python3 -m py_compile lambda_function.py
```

The command completed without errors.

## Key Concepts

- Amazon S3
- AWS Lambda
- S3 Event Notifications
- IAM execution roles
- Python Lambda functions
- Serverless processing
- CSV processing
- S3 input and output
- Event-driven architecture

## Result

The sales CSV stored in Amazon S3 was successfully processed using AWS Lambda, and the category-wise revenue was written back to Amazon S3 as a CSV file.

This practice demonstrates an event-driven serverless data-processing workflow using **Amazon S3 + AWS Lambda**.
