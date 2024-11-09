# exchange_data/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import BinanceData
from .utils import fetch_binance_data

def update_crypto_data():
    # Define the symbol you want to track
    symbol = 'BTCUSDT'

    # Fetch latest data from Binance
    binance_data = fetch_binance_data(symbol=symbol)
    if binance_data and len(binance_data) > 0:
        candlestick = binance_data[0]
        close_price = float(candlestick[4])

        # Save the data to the database
        BinanceData.objects.create(
            symbol=symbol,
            price=close_price
        )
        
        print(f"Data for {symbol} updated at {timezone.now()}")
    else:
        print("Failed to fetch data from Binance")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_crypto_data, 'interval', hours=1)
    scheduler.start()