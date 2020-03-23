from django.shortcuts import render
from rest_framework import viewsets, permissions

from apps.trade.models import Equity, Price
from apps.trade.serializers import EquitySerializer, PriceSerializer

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer
    # permission_classes = [permissions.IsAuthenticated]

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    # permission_classes = [permissions.IsAuthenticated]
