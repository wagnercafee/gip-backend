from fastapi import FastAPI
from src.routes import upload_investments
from src.database.connection import connect_db
from src.utils.search_quotes import search_quotes
from pydantic import BaseModel
from typing import List


app = FastAPI()


@app.get("/")
def read_root():
    return "GIP-Rodando!"


# Incluindo o router do upload
app.include_router(upload_investments.router)


@app.get("/test-db")
async def test_db():
    try:
        conn = await connect_db()
        await conn.execute("SELECT 1")
        await conn.close()
        return {"status": "Conexão com o banco funcionando"}
    except Exception as e:
        return {"error": str(e)}


class TickerRequest(BaseModel):
    tickers: List[str]


@app.post("/search-quotes")
async def teste(request: TickerRequest):
    try:
        resultado = await search_quotes(request.tickers)
        return {"Tickers": resultado}
    except Exception as e:
        return {"error": str(e)}
