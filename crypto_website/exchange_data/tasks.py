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
        # Clear existing data
        BinanceData.objects.filter(symbol=symbol).delete()
        
        # Bulk create new records from unique data
        bulk_data = [
            BinanceData(
                symbol=symbol,
                price=point['price'],
                timestamp=point['timestamp']
            )
            for point in binance_data
        ]
        BinanceData.objects.update_or_create(bulk_data)

def start_scheduler():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(update_crypto_data, 'interval', hours=1)
    scheduler.add_job(update_crypto_data, 'interval', minutes=1)
    scheduler.start()