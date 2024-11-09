# exchange_data/views.py
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from decimal import Decimal
import json
from datetime import datetime, timedelta
from .models import BinanceData
from .utils import fetch_binance_data, fetch_historical_binance_data

def data_table(request):
    # Fetch all BinanceData entries, ordered by timestamp
    data_entries = BinanceData.objects.all().order_by('-timestamp')

    # Render the data in the 'data_table.html' template
    return render(request, 'data_table.html', {'data_entries': data_entries})

def index(request):
    symbol = 'BTCUSDT'
    
    # Count existing data points
    existing_count = BinanceData.objects.filter(symbol=symbol).count()
    
    if existing_count < 100:
        # If we have less than 100 points, fetch historical data
        historical_data = fetch_historical_binance_data(symbol)
        
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
    
    # Get recent data and format it for the template
    recent_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp').first()
    
    if recent_data:
        # Convert the integer timestamp to a datetime object
        recent_data_dict = {
            'symbol': recent_data.symbol,
            'price': recent_data.price,
            'timestamp': recent_data.timestamp
        }
    else:
        recent_data_dict = None

    # Get historical data for the chart - limit to latest 100 points
    historical_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp')[:100]
    price_history = [
        {
            'timestamp': entry.timestamp,
            'price': float(entry.price)
        }
        for entry in reversed(historical_data)  # Reverse to show oldest to newest
    ]
    
    context = {
        'recent_data': recent_data_dict,
        'price_history': json.dumps(price_history, cls=DjangoJSONEncoder)
    }
    return render(request, 'exchange_data/index.html', context)

# View to clear the data
def clear_data(request):
    if request.method == "POST":
        # Clear all data from the model (adjust this according to your models)
        BinanceData.objects.all().delete()
        # Optionally, you can clear more models, or reset the database entirely
        # OtherModel.objects.all().delete()

        # Redirect to the /data_table after clearing the data
        return redirect('data_table')  # Adjust this to your actual data page URL

    # If the request isn't POST, render the confirmation page (optional)
    return render(request, 'clear_data_confirmation.html')