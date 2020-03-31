from rest_framework import serializers
from apps.trade.models import EquityIndex, Equity, Treasury


class EquityIndexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EquityIndex
        fields = ('url', 'name', 'ticker', 'industry', 'query', 'own')

class EquitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equity
        fields = ('url', 'date', 'asset', 'price',
                  'bid', 'ask', 'volume', 'marketcap')

class TreasurySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Treasury
        fields = ('url', 'date', 'type', 'maturity', 'price', 'ytm')
