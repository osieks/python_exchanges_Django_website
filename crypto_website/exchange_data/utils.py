# exchange_data/utils.py
from decimal import Decimal
import requests

def fetch_binance_data(symbol, interval='1h', limit=1):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        return [{'timestamp': candlestick[0], 'price': candlestick[4]} for candlestick in data]
    else:
        print(f"Error fetching data from Binance: {response.status_code}")
        return None

def fetch_historical_binance_data(symbol):
    # Fetch last 100 hourly candles
    data = fetch_binance_data(symbol, interval='1h', limit=168)
    print(data)
    if data:
        return data
    return None