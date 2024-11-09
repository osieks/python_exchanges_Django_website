from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import update_crypto_data

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Schedule the update_crypto_data function to run every hour
    scheduler.add_job(update_crypto_data, 'interval', hours=1)
    
    # Start the scheduler
    scheduler.start()
    
    print("Scheduler started. Task scheduled to run every hour.")
