import csv
import io
import urllib.parse
import boto3
from collections import defaultdict

s3 = boto3.client("s3")


def lambda_handler(event, context):
    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"],
        encoding="utf-8"
    )

    print(f"Processing: s3://{bucket}/{key}")

    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    csv_content = response["Body"].read().decode("utf-8")

    category_revenue = defaultdict(float)

    reader = csv.DictReader(io.StringIO(csv_content))

    for row in reader:
        quantity = int(row["quantity"])
        price = float(row["price"])
        revenue = quantity * price
        category_revenue[row["category"]] += revenue

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["category", "total_revenue"])

    for category in sorted(category_revenue):
        writer.writerow([
            category,
            int(category_revenue[category])
        ])

    output_key = "output/lambda/category_sales.csv"

    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=output.getvalue().encode("utf-8"),
        ContentType="text/csv"
    )

    print(f"Output written to s3://{bucket}/{output_key}")

    return {
        "statusCode": 200,
        "body": {
            "input": f"s3://{bucket}/{key}",
            "output": f"s3://{bucket}/{output_key}",
            "category_revenue": dict(category_revenue)
        }
    }
