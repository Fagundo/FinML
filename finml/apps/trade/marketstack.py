'''Scripts to query MarketStack'''
import os
import requests

MARKETSTACK_BASE = 'https://api.marketstack.com/v1'

assert 'MARKETSTACK_TOKEN' in os.environ.keys(), 'Set MARKETSTACK_TOKEN environment variable'
TOKEN = os.environ['MARKETSTACK_TOKEN']
ACCESS_KEY = f'?access_key={TOKEN}'


def intraday(stock_list, interval='15min', limit=2, offset=0):

    # Check API query values
    assert interval in ['15min', '30min', '1h', '3h', '6h', '12h'], 'Wrong interval'
    assert len(stock_list)<=20, 'Cannot query more than 20 stocks'

    total_limit = len(stock_list) * limit
    assert total_limit < 100, 'Unable to query more than 100 items'

    query = f'intraday{ACCESS_KEY}' + \
        f'&symbols={",".join(stock_list)}' + \
        f'&interval={interval}' + \
        f'&limit={total_limit}' + \
        f'&offset={offset}'

    try:
        response = requests.get(
            os.path.join(MARKETSTACK_BASE, query)
        )

        json_response = response.json()

        return json_response

    except Exception as e:
        print('Unable to query: ')
        print(str(e))

def tickers():
    query = f'tickers{ACCESS_KEY}'

    try:
        print(os.path.join(MARKETSTACK_BASE, query))
        response = requests.get(
            os.path.join(MARKETSTACK_BASE, query)
        )

        json_response = response.json()

        return json_response

    except Exception as e:
        raise
