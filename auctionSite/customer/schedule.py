from apscheduler.schedulers.background import BackgroundScheduler

from .views import removingItem

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(removingItem, 'interval',minutes = 1,id = 'rem001', replace_existing=True)
    scheduler.start()