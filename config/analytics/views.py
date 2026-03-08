from django.shortcuts import render
from .models import BettingOdds
from .serializers import BettingOddsSerializer
from rest_framework import viewsets

# Create your views here.

class BettingOddsViewSet(viewsets.ModelViewSet):
    queryset = BettingOdds.objects.select_related("match")
    serializer_class = BettingOddsSerializer