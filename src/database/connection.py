import asyncpg
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


async def get_db_connection():
    try:
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
        return conn
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao conectar ao banco de dados: {str(e)}")

# async def get_db_connection():
#     """
#     Retorna uma conexão com o banco de dados.
#     """
#     try:
#         conn = await asyncpg.connect(
#             host="localhost",  # Substitua pelo valor de DB_HOST
#             port=9091,         # Substitua pelo valor de DB_PORT
#             database="gipdb",  # Substitua pelo valor de DB_NAME
#             user="gipuser",    # Substitua pelo valor de DB_USER
#             password="gippass" # Substitua pelo valor de DB_PASS
#         )
#         return conn
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco de dados: {str(e)}")
