from celery import shared_task
import time

@shared_task()
def run():
    while True:
        print('_______THIS IS A TEST_________')
        time.sleep(2)
