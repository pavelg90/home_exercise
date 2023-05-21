import boto3
import os
import pandas as pd
from sqlalchemy import create_engine
from io import StringIO

# Set up MinIO client
s3 = boto3.resource('s3',
                  endpoint_url='http://s3_simulator:9000',
                  aws_access_key_id='minio',
                  aws_secret_access_key='minio123')

# Set up SQLAlchemy engine
engine = create_engine('postgresql://admin:admin@db:5432/')

# Download CSV files from MinIO and load them into the PostgreSQL database
def load_csvs_from_minio_to_db():
    for obj in s3.list_objects(Bucket='mybucket')['Contents']:
        try:
            filename = obj['Key']
            csv_obj = s3.get_object(Bucket='mybucket', Key=filename)
            body = csv_obj['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(body))
            table_name = os.path.splitext(filename)[0]  # Use the CSV filename (without extension) as the table name
            df.to_sql(table_name, engine, if_exists='replace')
        except:
            print('Something bad happened, or not...')

if __name__ == "__main__":
    load_csvs_from_minio_to_db()
