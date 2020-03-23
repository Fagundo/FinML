from rest_framework import serializers
from apps.trade.models import Price, Equity


class EquitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equity
        fields = ('url', 'name', 'ticker', 'industry')

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = ('url', 'date', 'asset', 'price', 'volume')
