'''Scripts to query MarketStack'''
import os
import requests

BASE_URL = 'https://cloud.iexapis.com'
VERSION = 'v1'

assert 'IEX_TOKEN' in os.environ.keys(), 'Set IEX_TOKEN environment variable'
TOKEN = os.environ['IEX_TOKEN']
ACCESS_KEY = f'?token={TOKEN}'

def get_query(query):
    try:
        response = requests.get(
            os.path.join(BASE_URL, VERSION, query)
        )

        json_response = response.json()

        return json_response

    except Exception as e:
        print(f'Unable to query {query}')
        print(str(e))


def quote(stock):
    query = os.path.join(
        'stock', stock.lower(), f'quote{ACCESS_KEY}'
    )

    return get_query(query)


def openclose():
    query = os.path.join(
        'stock', 'market', f'ohlc{ACCESS_KEY}'
    )

    return get_query(query)


def tickers():
    query = f'ref-data/iex/symbols{ACCESS_KEY}'

    return get_query(query)
