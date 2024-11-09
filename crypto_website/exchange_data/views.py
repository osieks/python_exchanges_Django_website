# exchange_data/views.py
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
import json
from datetime import timedelta
from .models import BinanceData
from .utils import fetch_binance_data, fetch_historical_binance_data

def index(request):
    symbol = 'BTCUSDT'
    
    # Count existing data points
    existing_count = BinanceData.objects.filter(symbol=symbol).count()
    
    if existing_count < 100:
        # If we have less than 100 points, fetch historical data
        historical_data = fetch_historical_binance_data(symbol)
        if historical_data:
            # Clear existing data
            BinanceData.objects.filter(symbol=symbol).delete()
            
            # Create a dictionary to store unique timestamp-price pairs
            unique_data = {}
            for point in historical_data:
                timestamp = timezone.datetime.fromtimestamp(
                    point['timestamp']/1000,
                    tz=timezone.get_current_timezone()
                )
                # Only keep the latest price for each timestamp
                unique_data[timestamp] = point['price']
            
            # Bulk create new records from unique data
            bulk_data = [
                BinanceData(
                    symbol=symbol,
                    price=price,
                    timestamp=timestamp
                )
                for timestamp, price in unique_data.items()
            ]
            BinanceData.objects.bulk_create(bulk_data)
    
    # Get recent data and format it for the template
    recent_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp').first()
    
    if recent_data:
        recent_data_dict = {
            'symbol': recent_data.symbol,
            'price': float(recent_data.price),
            'timestamp': recent_data.timestamp.isoformat()
        }
    else:
        recent_data_dict = None

    # Get historical data for the chart - limit to latest 100 points
    historical_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp')[:100]
    price_history = [
        {
            'timestamp': entry.timestamp.isoformat(),
            'price': float(entry.price)
        }
        for entry in reversed(historical_data)  # Reverse to show oldest to newest
    ]
    
    context = {
        'recent_data': recent_data_dict,
        'price_history': json.dumps(price_history, cls=DjangoJSONEncoder)
    }
    return render(request, 'exchange_data/index.html', context)