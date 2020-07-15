from apps.trade.models import EquityIndex, Equity
from apps.trade import marketstack
from config.celery import celery_app

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from datetime import datetime as dt

import time

import os
import requests


logger = get_task_logger(__name__)

schedule = crontab(
    minute='*/15',
    hour='13-18',
    day_of_week='mon-fri'
)


def batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        try:
            yield lst[i:i+batch_size]
        except Exception as e:
            yield lst[i:]


@shared_task
def get_equities(batch):
    json_response = marketstack.intraday(batch)

    for equity in json_response['data']:
        try:
            equity_object = Equity.objects.create(
                asset = EquityIndex.objects.get(ticker=equity['symbol']),
                high = equity['high'],
                low = equity['low'],
                date = equity['date'],
            )
        except Exception as e:
            print(str(e))


@periodic_task(run_every=schedule)
def query_equities():

    equities = EquityIndex.objects.filter(query=True)
    equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

    for batch in batches(equities, 20):
        get_equities(batch)
