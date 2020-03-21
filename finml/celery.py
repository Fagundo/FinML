import os
import celery
from celery import Celery

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_BROKER_URL= 'amqp://guest:guest@localhost:5672//'

celery_app = Celery('test', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)

if __name__ == '__main__':
    celery_app.autodiscover_tasks()
    celery_app.start()
