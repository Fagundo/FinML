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
def run_batch(function, batch):
    _ = list(map(function, batch))


def get_intraday(ticker):

    json_response = iex.quote(ticker)

    try:
        equity_object = IntraDay.objects.create(
            asset = EquityIndex.objects.get(ticker=json_response['symbol']),
            date=make_aware(dt.now()),
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

    while dt.now().hour < 18:
        equities = EquityIndex.objects.filter(query=True)
        equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

        for batch in batches(equities, 20):
            run_batch(get_intraday, batch)

        time.sleep(60) # Sleep 1 minute


@periodic_task(run_every=crontab(minute='30', hour='18', day_of_week='mon-fri'))
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
                    date = make_aware(dt.now()),
                    asset = EquityIndex.objects.get(ticker=k),
                    open = v['open']['price'],
                    close = v['close']['price'],
                    low = v['low'],
                    high = v['high'],
                    volume = v['volume']
                )

                equities.remove(k)

            except Exception as e:
                print(str(e))
