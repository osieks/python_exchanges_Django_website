# exchange_data/views.py
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from decimal import Decimal
import json
from datetime import datetime, timedelta
from .models import BinanceData
from .utils import fetch_binance_data
from .tasks import update_crypto_data
from django.http import HttpResponse

def data_table(request):
    # Fetch all BinanceData entries, ordered by timestamp
    data_entries = BinanceData.objects.all().order_by('-timestamp')

    # Render the data in the 'data_table.html' template
    return render(request, 'data_table.html', {'data_entries': data_entries})

def index(request):
    symbol = 'BTCUSDT'

    recent_data = BinanceData.objects.last()
    # Get the data limit from the request, or default
    data_limit = request.GET.get('data_limit', '48')
    
    try:
        data_limit = int(data_limit)
    except ValueError:
        data_limit = 48  # Fallback to default if parsing fails
    

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

    # Get all data if 'data_limit' is set to a special value like -1
    if data_limit == -1:
        historical_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp')
    else:
        historical_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp')[:(data_limit)]
    # Get historical data for the chart - limit to latest x points
    #historical_data = BinanceData.objects.filter(symbol=symbol).order_by('-timestamp')[:168]
    price_history = [
        {
            'timestamp': entry.timestamp,
            'price': float(entry.price)
        }
        for entry in reversed(historical_data)  # Reverse to show oldest to newest
    ]
    
    context = {
        'recent_data': recent_data_dict,
        'price_history': json.dumps(price_history, cls=DjangoJSONEncoder),
        'data_limit': data_limit
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
    return render(request, 'clear_data_confirmation.html')# View to clear the data

def update_data(request):
    if request.method == "POST":
        # Get the number of data points from the form
        data_points = request.POST.get('data_points', 168)  # Default to 168 if not provided
        try:
            data_points = int(data_points)  # Convert to an integer
        except ValueError:
            return HttpResponse("Invalid number of data points", status=400)

        # Call the function to update the crypto data
        update_crypto_data(limit=data_points)  # Pass the user-defined limit to the task

        return redirect('data_table')  # Redirect to the data_table page after updating

    return render(request, 'clear_data_confirmation.html')  # Render a confirmation page if not a POST request