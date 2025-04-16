import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def connect_db():
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
    )
    return conn
