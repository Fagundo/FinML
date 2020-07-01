from apps.trade.models import EquityIndex, Equity
from apps.trade import marketstack
from config.celery import celery_app

from django.forms.models import model_to_dict
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from datetime import datetime as dt
from django.utils import timezone

import time

import os
import requests


logger = get_task_logger(__name__)


def batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        try:
            yield lst[i:i+batch_size]
        except Exception as e:
            yield lst[i:]

@periodic_task(run_every=crontab(hour='13', minute='29', day_of_week='mon,tue,wed,thu,fri'))
def get_equities():

    equities = EquityIndex.objects.filter(query=True)
    equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

    for batch in batches(equities, 20):
        json_response = marketstack.intraday(batch)

        for equity in json_response['data']:
            equity_object = Equity.objects.create(
                asset = EquityIndex.objects.get(ticker=equity['symbol']),
                high = equity['high'],
                low = equity['low'],
                date = equity['date'],
            )
