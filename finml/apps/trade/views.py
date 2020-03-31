from django.shortcuts import render
from rest_framework import viewsets, permissions

from apps.trade.models import EquityIndex, Equity, Treasury
from apps.trade.serializers import EquityIndexSerializer, EquitySerializer, TreasurySerializer

class EquityIndexViewSet(viewsets.ModelViewSet):
    queryset = EquityIndex.objects.all()
    serializer_class = EquityIndexSerializer
    # permission_classes = [permissions.IsAuthenticated]

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer
    # permission_classes = [permissions.IsAuthenticated]

class TreasuryViewSet(viewsets.ModelViewSet):
    queryset = Treasury.objects.all()
    serializer_class = TreasurySerializer
    # permission_classes = [permissions.IsAuthenticated]
