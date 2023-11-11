from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api

# def start():
# 	scheduler = BackgroundScheduler()
# 	scheduler.add_job(schedule_api, 'interval', seconds=5)
# 	scheduler.start()

def start():
    scheduler = BackgroundScheduler()
    # Schedule the task to run every day at 10:00 AM
    #Eg;System check identified 1 issue (0 silenced).
    #October 16, 2023 - 00:03:48
    scheduler.add_job(schedule_api, 'cron', hour=00, minute=5)
    scheduler.start()