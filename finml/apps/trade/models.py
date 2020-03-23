from django.db import models

# Create your models here.

class Equity(models.Model):
    name = models.CharField(max_length=20, help_text='Equity Name')
    ticker = models.CharField(max_length=4, help_text='Equity Ticker Symbol',
                              primary_key=True)
    industry = models.CharField(max_length=20, help_text='Equity Industry',
                                blank=True, null=True)
    industry_2 = models.CharField(max_length=20, help_text='Equity Industry 2',
                                blank=True, null=True)
    industry_3 = models.CharField(max_length=20, help_text='Equity Industry 3',
                                blank=True, null=True)


class Price(models.Model):
    date = models.DateTimeField()
    asset = models.ForeignKey(Equity, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    volume = models.IntegerField()
