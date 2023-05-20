from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

engine = create_engine('postgresql://admin:admin@db:5432/dbname')

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.get("/{id}")
def read_item(id: int):
    with engine.connect() as connection:
        result = connection.execute(f"SELECT * FROM users WHERE ID = {id}")
        row = result.fetchone()
        return {"id": row[0], "name": row[1]} if row else {"message": "User not found"}
