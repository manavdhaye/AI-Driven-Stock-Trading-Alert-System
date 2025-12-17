# data_fetcher.py
import requests
import pandas as pd
from config import ALPHA_VANTAGE_KEY

def fetch_stock_data(symbol):
    """Fetch daily stock data from Alpha Vantage"""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    data = response.json().get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(data, orient="index", dtype=float)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    }, inplace=True)
    return df

# print(fetch_stock_data("RELIANCE.BSE"))
