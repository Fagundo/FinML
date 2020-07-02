from rest_framework import serializers
from apps.trade.models import EquityIndex, OpenClose, IntraDay


class EquityIndexSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        view_name="equityindex-detail", read_only=True
    )

    class Meta:
        model = EquityIndex
        fields = ('url', 'name', 'ticker', 'sector', 'enabled', 'query', 'own')

class OpenCloseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenClose
        fields = ('url', 'date', 'asset', 'open', 'close', 'high', 'low')

class IntraDaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IntraDay
        fields = ('url', 'date', 'asset', 'update_date', 'price',
                  'peratio', 'bid', 'ask', 'volume', 'source')
