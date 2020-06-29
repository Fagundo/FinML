import os
import pandas as pd
from apps.trade.models import EquityIndex
from django.core.management.base import BaseCommand, CommandError

CWD = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(CWD, 'sp_data')

WTD_TICKER_DIR = os.path.join(DATA_DIR, 'wtd_ticker.txt')
SP_DIR = os.path.join(DATA_DIR, 'constituents.csv')

def get_wtd_tickers(wtd_data_path):
    replace_these = ['\n', '"', '^', '[', ']']

    with open(wtd_data_path) as f:
      tickers = f.readlines()
      tickers = tickers[0]
      for rep in replace_these:
          tickers =  tickers.replace(rep,'')

      return tickers.split(',')


class Command(BaseCommand):
    '''Add S&P stock metadata to Django'''

    def add_arguments(self, parser):
        parser.add_argument('-t', '--tickers', default=WTD_TICKER_DIR)
        parser.add_argument('-s', '--stocks', default=SP_DIR)

    def handle(self, *args, **options):
        tickers = get_wtd_tickers(options['tickers'])

        # Get S&P stock codes for WTD
        sp = pd.read_csv(options['stocks'])
        sp = sp[sp['Symbol'].isin(tickers)]

        for index, row in sp.iterrows():
            name = row['Name']
            ticker = row['Symbol']
            industry = row['Sector']
            try:
                EquityIndex.objects.get_or_create(name=name, ticker=ticker,
                                                  industry=industry)
            except Exception as e:
                print(e)
                print(f'Failed to create asset {name}')
