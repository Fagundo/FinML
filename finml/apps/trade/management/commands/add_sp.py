import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from apps.trade import iex
from apps.trade.models import EquityIndex


CWD = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CWD, 'sp_data')
SP_DIR = os.path.join(DATA_DIR, 'constituents.csv')


class Command(BaseCommand):
    '''Add S&P stock metadata to Django'''

    def add_arguments(self, parser):
        parser.add_argument('-s', '--stocks', default=SP_DIR)

    def handle(self, *args, **options):
        tickers = iex.tickers()

        # Get S&P stock codes for WTD
        sp = pd.read_csv(options['stocks'])
        enabled_tickers = [x['symbol'] for x in tickers if x['isEnabled']]

        sp = sp[sp['Symbol'].isin(enabled_tickers)]

        for _, stock in sp.iterrows():

            try:
                EquityIndex.objects.get_or_create(
                    name=stock['Name'],
                    ticker=stock['Symbol'],
                    sector=stock['Sector'],
                    enabled=True,
                )
                
            except Exception as e:
                name = stock['Name']
                print(f'Failed to create asset {name}')
                print(e)
