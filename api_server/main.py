import time
from fastapi import FastAPI
from sqlalchemy import create_engine, exc

app = FastAPI()

database_initialized = False
while not database_initialized:
    try:
        engine = create_engine('postgresql://admin:admin@db:5432/dbname')
        with engine.connect() as connection:
            # Try a simple query to check if connection is established
            connection.execute("SELECT 1")
            database_initialized = True
    except exc.DBAPIError as e:
        print("Database not ready yet, waiting...")
        time.sleep(5)

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.get("/{id}")
def read_item(id: int):
    with engine.connect() as connection:
        result = connection.execute(f"SELECT * FROM users WHERE ID = {id}")
        row = result.fetchone()
        return {"id": row[0], "name": row[1]} if row else {"message": "User not found"}
