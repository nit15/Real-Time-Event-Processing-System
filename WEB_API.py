from fastapi import FastAPI
import psycopg2
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; specify specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="sensor_db",
        user="postgres",
        password="153200",
    )
    return conn

@app.get("/sensors")
async def get_sensor_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_table LIMIT 100;")
    rows=cursor.fetchall()
    conn.close()
    return {"data":rows}
