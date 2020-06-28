import pandas as pd
from apps.trade.models import EquityIndex

df = pd.read_csv('sp_stocks.csv')

for index, row in df.iterrows():
    try:
        EquityIndex.objects.get_or_create(
            name=row['Name'],
            ticker=row['Symbol'],
            industry=row['Sector'],
        )
    except Exception as e:
        print(row)
        print(str(e))
