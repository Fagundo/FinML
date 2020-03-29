from django.shortcuts import render
from rest_framework import viewsets, permissions

from apps.trade.models import EquityIndex, Equity
from apps.trade.serializers import EquityIndexSerializer, EquitySerializer

class EquityIndexViewSet(viewsets.ModelViewSet):
    queryset = EquityIndex.objects.all()
    serializer_class = EquityIndexSerializer
    # permission_classes = [permissions.IsAuthenticated]

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer
    # permission_classes = [permissions.IsAuthenticated]
