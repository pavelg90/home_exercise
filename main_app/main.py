from sqlalchemy import create_engine
from minio.error import S3Error
from minio import Minio
from io import BytesIO
import pandas as pd
import time
import os


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "s3_simulator:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False,
    )

    engine = create_engine('postgresql://admin:admin@db:5432/dbname')

    # Specify the bucket name
    bucket_name = "mybucket"

    # Make 'mybucket' bucket if not exist.
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket {bucket_name} already exists")

    try:
        # List all object names in bucket
        objects = client.list_objects(bucket_name)

        for obj in objects:
            # Only process CSV files
            if obj.object_name.endswith('.csv'):
                # Get the CSV data
                data = client.get_object(bucket_name, obj.object_name)

                # Load CSV data into a DataFrame
                df = pd.read_csv(BytesIO(data.read()))

                # Use CSV file name (without extension) as table name
                table_name = obj.object_name

                # Write DataFrame to PostgreSQL table
                df.to_sql(table_name, engine, if_exists='replace')

                # Delete the file from the bucket after it has been processed
                client.remove_object(bucket_name, obj.object_name)

    except S3Error as err:
        print(f"Error: {err}")



if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("error occurred.", e)

        time.sleep(1)
