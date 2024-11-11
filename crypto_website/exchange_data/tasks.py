# exchange_data/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import BinanceData
from .utils import fetch_binance_data

def update_crypto_data(symbol = 'BTCUSDT', interval='1h', limit=1):
    # Define the symbol you want to track
    

    # Count existing data points
    existing_count = BinanceData.objects.filter(symbol=symbol).count()
    
    if existing_count < 100:
        if limit < 100:
            limit = 100
        # If we have less than x points, fetch historical data
        historical_data = fetch_binance_data(symbol,interval,limit=limit)
        
        if len(historical_data) != 0:
            # Clear existing data
            BinanceData.objects.filter(symbol=symbol).delete()
            
            # Bulk create new records from unique data
            bulk_data = [
                BinanceData(
                    symbol=symbol,
                    price=point['price'],
                    timestamp=point['timestamp']
                )
                for point in historical_data
            ]
            BinanceData.objects.bulk_create(bulk_data)
    else:

        # Fetch latest data from Binance
        binance_data = fetch_binance_data(symbol=symbol)
        
        if binance_data and len(binance_data) > 0:
            for point in binance_data:
                # Use update_or_create for each individual data point
                BinanceData.objects.update_or_create(
                    symbol=symbol,
                    timestamp=point['timestamp'],
                    defaults={'price': point['price']}  # 'defaults' is used for fields to update
                )
        

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_crypto_data, 'interval', hours=1)
    #scheduler.add_job(update_crypto_data, 'interval', minutes=10)
    scheduler.start()