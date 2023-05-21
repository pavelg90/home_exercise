from sqlalchemy import create_engine
import boto3
from io import BytesIO
import pandas as pd
import time
import os


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    s3_target = boto3.resource(
        's3',
        endpoint_url='http://192.168.96.3:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='minio123',
        aws_session_token=None,
        config=boto3.session.Config(signature_version='s3v4'),verify=False)

    engine = create_engine('postgresql://admin:admin@db:5432/dbname')

    for bucket in s3_target.buckets.all():
        bucket_name = bucket.name
        for bucket in s3_target.buckets.all():
            for file in bucket.objects.all():
                filename = file.key
                if '.csv' in filename:
                    response = s3_target.Object(bucket_name, filename).get()
                    df = pd.read_csv(BytesIO(response['Body'].read()))

                    # Write to table
                    df.to_sql(filename, engine, if_exists='replace')

                    # Delete file:
                    s3_target.Object(bucket_name, filename).delete()


if __name__ == "__main__":
    print('Running')
    while True:
        try:
            main()
        except Exception as e:
            print("error occurred.", e)

        time.sleep(1.5)
