from django.shortcuts import render
from .models import BettingOdds
from .serializers import BettingOddsSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Create your views here.

class BettingOddsViewSet(viewsets.ModelViewSet):
    queryset = BettingOdds.objects.select_related("match").all()
    serializer_class = BettingOddsSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["match"]

    ordering_fields = ["match__match_date"]
    ordering = ["-match__match_date"]