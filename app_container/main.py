import os
import time
import glob
import pandas as pd
from sqlalchemy import create_engine, exc

database_initialized = False
while not database_initialized:
    try:
        engine = create_engine('postgresql://admin:admin@db:5432/dbname')
        with engine.connect() as connection:
            with connection.begin():
                # Try a simple query to check if connection is established
                connection.execute("SELECT 1")
                database_initialized = True
    except exc.DBAPIError as e:
        print("Database not ready yet, waiting...")
        time.sleep(5)

print("Database connection established.")

while True:
    for file in glob.glob("/app/data/*.csv"):
        try:
            # Read CSV file into a DataFrame
            df = pd.read_csv(file)

            # Write DataFrame to PostgreSQL
            df.to_sql(os.path.basename(file), engine, if_exists='replace')

            print(f"Loaded file {file} into database.")

            # Delete file after loading
            os.remove(file)
            print(f"Deleted file {file}.")
        except Exception as e:
            print(f"Failed to process file {file}: {str(e)}")
    time.sleep(5)
