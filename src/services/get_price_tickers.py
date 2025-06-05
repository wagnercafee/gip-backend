import yfinance as yf

async def get_price_tickers(tickers: list[str]) -> dict:
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                prices[ticker] = round(price, 2)
            else:
                prices[ticker] = "Sem dados"
        except Exception as e:
            prices[ticker] = f"Erro: {str(e)}"
    return prices
