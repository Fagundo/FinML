from django.db import models


class EquityIndex(models.Model):
    '''Django model of equity assets. Includes generic information about the asset.
       Primarily used as an index for equities to query'''
    name = models.CharField(max_length=40, help_text='Equity Name')
    ticker = models.CharField(max_length=6, help_text='Equity Ticker Symbol',
                              primary_key=True)
    sector = models.CharField(max_length=40, help_text='Equity Sector',
                                blank=True, null=True)
    enabled =  models.BooleanField(default=True)
    query = models.BooleanField(default=True)
    own = models.BooleanField(default=False)


class OpenClose(models.Model):
    date = models.DateTimeField()
    asset = models.ForeignKey(EquityIndex, on_delete=models.CASCADE)
    open = models.FloatField(null=True, blank=True)
    close = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)


class IntraDay(models.Model):
    date = models.DateTimeField()
    asset = models.ForeignKey(EquityIndex, on_delete=models.CASCADE)
    update_date = models.DateTimeField()
    price = models.FloatField(null=True, blank=True)
    peratio = models.FloatField(null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)
    ask = models.FloatField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=25, help_text='Quote Source',
                              blank=True, null=True)
