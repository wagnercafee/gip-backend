import yfinance as yf


async def search_quotes(tickers: list[str]) -> dict:
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
