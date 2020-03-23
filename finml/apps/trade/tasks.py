from apps.trade.models import Equity, Price
from config.celery import celery_app

from django.forms.models import model_to_dict
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from datetime import datetime as dt
from django.utils import timezone
import time
import random


logger = get_task_logger(__name__)

@celery_app.task(ignore_result=True)
def test(self):
    print('Hello World')

@periodic_task(run_every=crontab(minute='*'))
def get_equities():
    equities = Equity.objects.all()
    for equity in equities:
        # QUERY HERE
        logger.debug(f'NAME: {str(equity.name)}')
        logger.debug(f'TICKER: {str(equity.ticker)}\n')

# @celery_app.task(ignore_result=True)
@periodic_task(run_every=crontab(minute='*'))
def stock_query():
    equity_1=None

    try:
        equity_1, exists = Equity.objects.get_or_create(
            name='Josh Luxton',
            ticker='JL',
            industry='datascience',
            industry_2='dad',
        )
        logger.debug('SUCCESSS')
        logger.debug(str(model_to_dict(equity_1)))

    except Exception as e:
        logger.debug('FAILURE')
        logger.debug(str(e))

    try:
        equity_price = Price.objects.create(
            date=dt.now(tz=timezone.utc),
            asset=equity_1,
            price=random.random(),
            volume=1
        )
        equity_price.save()

        logger.debug('SUCCESS__PRICE___')
        logger.debug(str(model_to_dict(equity_price)))

    except Exception as e:
        logger.debug('FAILURE__PRICE___')
        logger.debug(str(e))
