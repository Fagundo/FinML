import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from apps.trade import marketstack
from apps.trade.models import EquityIndex


CWD = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CWD, 'sp_data')
SP_DIR = os.path.join(DATA_DIR, 'constituents.csv')


class Command(BaseCommand):
    '''Add S&P stock metadata to Django'''

    def add_arguments(self, parser):
        parser.add_argument('-s', '--stocks', default=SP_DIR)

    def handle(self, *args, **options):
        tickers = marketstack.tickers()

        # Get S&P stock codes for WTD
        sp = pd.read_csv(options['stocks'])
        sp_symbols = sp['Symbol'].tolist()

        sp_data = list(
            filter(lambda x: x['symbol'] in sp_symbols, tickers['data'])
        )


        for stock in sp_data:

            try:
                EquityIndex.objects.get_or_create(
                    name=stock['name'],
                    ticker=stock['symbol'],
                    currency=stock['stock_exchange']['currency']['code'],
                    exchange=stock['stock_exchange']['acronym'],
                )

            except Exception as e:
                name = stock['name']
                print(f'Failed to create asset {name}')
                print(e)
