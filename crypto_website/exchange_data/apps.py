# exchange_data/apps.py
from django.apps import AppConfig

class ExchangeDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange_data'

    def ready(self):
        from . import tasks
        tasks.start_scheduler()