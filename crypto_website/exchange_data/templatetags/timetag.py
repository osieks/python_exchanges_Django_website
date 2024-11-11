from django import template
import datetime

# Register the template filter library
register = template.Library()

# Define the custom filter function
def print_timestamp(timestamp):
    try:
        # Assume timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except (ValueError, TypeError):
        return None
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Register the filter with the name "print_timestamp"
register.filter('print_timestamp', print_timestamp)
