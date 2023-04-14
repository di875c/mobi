import time
from django.apps import AppConfig
from threading import Thread
import datetime


class DBUpdateThread(Thread):
    '''
    daemon thread for DB update every 24 hours
    '''
    daemon = True

    def run(self) -> None:
        from currency.views import get_currency
        while True:
            data = get_currency(datetime.datetime.now().date())
            time.sleep(24 * 60 * 60)


class MobiConfig(AppConfig):
    '''
    start DBUpdate thread when configuration task
    '''
    name = 'mobi'

    def ready(self):
        DBUpdateThread().start()
