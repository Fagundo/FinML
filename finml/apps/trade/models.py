from django.db import models


class EquityIndex(models.Model):
    '''Django model of equity assets. Includes generic information about the asset.
       Primarily used as an index for equities to query'''
    name = models.CharField(max_length=40, help_text='Equity Name')
    ticker = models.CharField(max_length=6, help_text='Equity Ticker Symbol',
                              primary_key=True)
    industry = models.CharField(max_length=40, help_text='Equity Industry',
                                blank=True, null=True)
    currency =  models.CharField(max_length=6, help_text='Equity Currency',
                                 blank=True, null=True)
    exchange = models.CharField(max_length=6, help_text='Equity Exchange',
                                 blank=True, null=True)
    query = models.BooleanField(default=True)
    own = models.BooleanField(default=False)


class Equity(models.Model):
    date = models.DateTimeField()
    asset = models.ForeignKey(EquityIndex, on_delete=models.CASCADE)
    low = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)

# TODO MJF: Make a model for brokerage accounts
# class Broker(models.Model):
#     brokerage = models.CharField(max_length=20, help_text='Equity Name')
#     asset = models.CharField(max_length=20, help_text='Equity Name')
#     username = models.CharField(max_length=20, help_text='Equity Name')
#     token = models.CharField(max_length=20, help_text='Equity Name')
