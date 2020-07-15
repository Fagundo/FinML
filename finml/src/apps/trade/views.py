from django.shortcuts import render
from rest_framework import viewsets, permissions

from apps.trade.models import EquityIndex, OpenClose, IntraDay
from apps.trade.serializers import EquityIndexSerializer, OpenCloseSerializer,\
    IntraDaySerializer

class EquityIndexViewSet(viewsets.ModelViewSet):
    queryset = EquityIndex.objects.all()
    serializer_class = EquityIndexSerializer
    # permission_classes = [permissions.IsAuthenticated]

class OpenCloseViewSet(viewsets.ModelViewSet):
    queryset = OpenClose.objects.all()
    serializer_class = OpenCloseSerializer
    # permission_classes = [permissions.IsAuthenticated]

class IntraDayViewSet(viewsets.ModelViewSet):
    queryset = IntraDay.objects.all()
    serializer_class = IntraDaySerializer
    # permission_classes = [permissions.IsAuthenticated]
