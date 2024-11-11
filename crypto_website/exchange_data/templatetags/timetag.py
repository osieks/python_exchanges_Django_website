from django import template
import time
from datetime import datetime
import pytz

# Register the template filter library
register = template.Library()

# Define the custom filter function
def print_timestamp(timestamp):

    naive_datetime = datetime.utcfromtimestamp(timestamp/1000)
    localized_datetime = naive_datetime.astimezone(pytz.timezone('Europe/Warsaw'))
    return localized_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Register the filter with the name "print_timestamp"
register.filter('print_timestamp', print_timestamp)
