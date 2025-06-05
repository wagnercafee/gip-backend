from fastapi import FastAPI
from src.routes import upload_investments, search_quotes
from src.database.connection import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return "GIP-Rodando!"

# Incluindo o router do upload
app.include_router(upload_investments.router)
app.include_router(search_quotes.router)

@app.get("/test-db")
async def test_db():
    try:
        conn = await get_db_connection()
        await conn.execute("SELECT 1")
        await conn.close()
        return {"status": "Conexão com o banco funcionando"}
    except Exception as e:
        return {"error": str(e)}
