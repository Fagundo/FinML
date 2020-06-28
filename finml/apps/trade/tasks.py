from apps.trade.models import EquityIndex, Equity
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

def realtime(stock_list):
    req_str = 'https://api.worldtradingdata.com/api/v1/stock?symbol='
    try:
        response = requests.get(
            req_str+','.join(stock_list)+'&api_token='+os.environ['WORLDTRADE_TOKEN']
            )
        json_response = response.json()

        return json_response

    except Exception as e:
        print(str(e))

@periodic_task(run_every=crontab(hour='13', minute='29', day_of_week='mon,tue,wed,thu,fri'))
def get_equities():

    date = dt.now()
    end_trading = dt(date.year, date.month, date.day, 20, 0, 1, 0)

    while dt.now() < end_trading :
        equities = EquityIndex.objects.filter(query=True)
        equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

        for batch in batches(equities, 50):
            json_response = realtime(batch)

            for equity in json_response['data']:
                equity_object = Equity.objects.create(
                    asset = EquityIndex.objects.get(ticker=equity['symbol']),
                    price = equity['price'],
                    volume = equity['volume'] if isinstance(equity['volume'], int) else None,
                    marketcap = equity['market_cap'] if isinstance(equity['market_cap'], int) else None,
                    eps = equity['eps'] if isinstance(equity['eps'], float) else None,
                    pe = equity['pe'] if isinstance(equity['pe'], float) else None,
                )
        time.sleep(30)
