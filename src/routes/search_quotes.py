from src.services.get_price_tickers import get_price_tickers
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter

router = APIRouter()
class TickerRequest(BaseModel):
    tickers: List[str]

@router.post("/search-quotes")
async def teste(request: TickerRequest):
    try:
        resultado = await get_price_tickers(request.tickers)
        return {"Tickers": resultado}
    except Exception as e:
        return {"error": str(e)}
