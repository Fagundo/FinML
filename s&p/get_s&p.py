import pandas as pd

with open('wtd_ticker.txt') as f:
  tickers = f.readlines()
  tickers =  tickers[0].replace('\n','').replace('"','').replace('^','').replace('[','').replace(']','').split(',')


sp = pd.read_csv('constituents.csv')
queries = []
for symbol in sp.Symbol:
    ticks = [i for i in tickers if symbol==i]
    if len(ticks)>0:
        queries.append(ticks[0])


stocks = sp.loc[sp['Symbol'].isin(queries), :]
stocks.reset_index(inplace=True)
stocks.drop('index', axis=1, inplace=True)
stocks.to_csv('sp_stocks.csv')
