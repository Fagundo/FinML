from django.db import models


class EquityIndex(models.Model):
    '''Django model of equity assets. Includes generic information about the asset.
       Primarily used as an index for equities to query'''
    name = models.CharField(max_length=20, help_text='Equity Name')
    ticker = models.CharField(max_length=4, help_text='Equity Ticker Symbol',
                              primary_key=True)
    industry = models.CharField(max_length=20, help_text='Equity Industry',
                                blank=True, null=True)
    industry_2 = models.CharField(max_length=20, help_text='Equity Industry 2',
                                blank=True, null=True)
    industry_3 = models.CharField(max_length=20, help_text='Equity Industry 3',
                                blank=True, null=True)
    query = models.BooleanField(default=True)
    own = models.BooleanField(default=False)


class Equity(models.Model):
    date = models.DateTimeField()
    asset = models.ForeignKey(EquityIndex, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    volume = models.IntegerField()
    marketcap = models.IntegerField()

# TODO MJF: Make a model for brokerage accounts
# class Broker(models.Model):
#     brokerage = models.CharField(max_length=20, help_text='Equity Name')
#     asset = models.CharField(max_length=20, help_text='Equity Name')
#     username = models.CharField(max_length=20, help_text='Equity Name')
#     token = models.CharField(max_length=20, help_text='Equity Name')
