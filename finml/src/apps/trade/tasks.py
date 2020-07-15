from apps.trade.models import EquityIndex, IntraDay, OpenClose
from apps.trade import iex
from config.celery import celery_app

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

import os
import time
import requests
from datetime import datetime as dt

from django.utils import timezone
from django.utils.timezone import make_aware


logger = get_task_logger(__name__)


def batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        try:
            yield lst[i:i+batch_size]
        except Exception as e:
            yield lst[i:]


def convert_timestamp(timestamp):
    timestamp = dt.fromtimestamp(timestamp / 1000)
    timestamp.replace(year = timestamp.year + 1970)
    return make_aware(timestamp)


@shared_task
def run_batch(*args):
    _ = list(map(get_intraday, args))


def get_intraday(ticker):

    json_response = iex.quote(ticker)

    try:
        equity_object = IntraDay.objects.create(
            asset = EquityIndex.objects.get(ticker=json_response['symbol']),
            date=timezone.now(),
            update_date = convert_timestamp(json_response['latestUpdate']),
            price = json_response['latestPrice'],
            peratio = json_response['peRatio'],
            bid = json_response['iexBidPrice'],
            ask = json_response['iexAskPrice'],
            volume = json_response['latestVolume'],
            source = json_response['latestSource'],
        )

    except Exception as e:
        print(str(e))


@periodic_task(run_every=crontab(minute='30', hour='13',day_of_week='mon-fri'))
def query_intraday():
    start = timezone.now()

    while start.hour!=19 and start.minute<58:
        time_diff = timezone.now() - start

        if time_diff.seconds>=60:
            start = timezone.now()

            equities = EquityIndex.objects.filter(query=True)
            equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

            for batch in batches(equities, 50):
                run_batch.apply_async(batch)

        else:
            time.sleep(int(60 - time_diff.seconds))



@periodic_task(run_every=crontab(hour='20', day_of_week='mon-fri'))
def query_open_close():

    equities = EquityIndex.objects.filter(query=True)
    equities = set([eq.ticker for eq in EquityIndex.objects.filter(query=True)])
    openclose = iex.openclose()

    for k, v in openclose.items():
        if k not in equities:
            continue
        else:
            try:
                openclose = OpenClose.objects.create(
                    date = timezone.now(),
                    asset = EquityIndex.objects.get(ticker=k),
                    open = v['open']['price'],
                    close = v['close']['price'],
                    low = v['low'],
                    high = v['high'],
                    volume = v['volume']
                )

            except Exception as e:
                print(str(e))
