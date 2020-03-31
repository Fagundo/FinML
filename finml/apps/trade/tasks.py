from apps.trade.models import EquityIndex, Equity, Treasury
from apps.trade.scrape import treasuries
from config.celery import celery_app

from django.forms.models import model_to_dict
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from datetime import datetime as dt
from django.utils import timezone

import os
import requests


logger = get_task_logger(__name__)


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

@periodic_task(run_every=crontab(minute='*'))
def get_equities():
    equities = EquityIndex.objects.filter(query=True)
    equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

    if len(equities) > 0:
        json_response = realtime(equities)

        for equity in json_response['data']:
            equity_object = Equity.objects.create(
                date = equity['last_trade_time'],
                asset = EquityIndex.objects.get(ticker=equity['symbol']),
                price = equity['price'],
                volume = equity['volume'],
                marketcap = equity['market_cap'],
                eps = equity['eps'],
                pe = equity['pe'] if isinstance(equity['pe'], float) else None,
            )

@periodic_task(run_every=crontab(minute='*'))
def get_treasuries():
    for treasury in treasuries.get():
        if treasury['type']!='muni':
            Treasury.objects.create(
                date = dt.strptime(treasury['time (edt)'], '%m/%d/%Y'),
                symbol = treasury['symbol'],
                type = treasury['type'],
                maturity = treasury['maturity'],
                coupon = treasury['coupon'],
                price = treasury['price'],
                ytm = treasury['yield'],
            )
        else:
            Treasury.objects.create(
                date = dt.strptime(treasury['time (edt)'], '%m/%d/%Y'),
                symbol = treasury['symbol'],
                type = treasury['type'],
                maturity = treasury['maturity'],
                ytm = treasury['yield'],
            )
