from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

engine = create_engine('postgresql://admin:admin@db:5432/dbname')

@app.get("/{id}")
def read_item(id: int):
    with engine.connect() as connection:
        result = connection.execute(f"SELECT * FROM users WHERE ID = {id}")
        return result.fetchone()
