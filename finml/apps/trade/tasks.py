from apps.trade.models import EquityIndex, Equity
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

@celery_app.task(ignore_result=True)
def test(self):
    print('Hello World')

@periodic_task(run_every=crontab(minute='*'))
def get_equities():
    equities = EquityIndex.objects.filter(query=True)
    equities = [eq.ticker for eq in EquityIndex.objects.filter(query=True)]

    if len(equities) > 0:
        json_response = realtime(equities)
        logger.debug(str(json_response))
    # for equity in equities:
    #     # TODO: MJF QUERY DATA
    #     logger.debug(f'NAME: {str(equity.name)}')
    #     logger.debug(f'TICKER: {str(equity.ticker)}\n')
#
# @periodic_task(run_every=crontab(minute='*'))
# def stock_query():
#
#
#     try:
#         equity_1, exists = Equity.objects.get_or_create(
#             name='Josh Luxton',
#             ticker='JL',
#             industry='datascience',
#             industry_2='dad',
#         )
#         logger.debug('SUCCESSS')
#         logger.debug(str(model_to_dict(equity_1)))
#
#     except Exception as e:
#         logger.debug('FAILURE')
#         logger.debug(str(e))
#
#     try:
#         p = random.uniform(1, 15)
#         equity_price = Price.objects.create(
#             date=dt.now(tz=timezone.utc),
#             asset=equity_1,
#             price=p,
#             bid=p-random.random(),
#             ask=p+random.random(),
#             volume=round(random.uniform(1000, 5000))
#         )
#         equity_price.save()
#
#         logger.debug('SUCCESS__PRICE___')
#         logger.debug(str(model_to_dict(equity_price)))
#
#     except Exception as e:
#         logger.debug('FAILURE__PRICE___')
#         logger.debug(str(e))
