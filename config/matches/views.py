from django.shortcuts import render
from rest_framework import viewsets
from .models import Match, PlayerMatchStats
from .serializers import MatchSerializer, PlayerMatchStatsSerializer

# Create your views here.

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related(
        "home_team",
        "away_team"
    )

    serializer_class = MatchSerializer


class PlayerMatchStatsViewSet(viewsets.ModelViewSet):

    queryset = PlayerMatchStats.objects.select_related(
        "player",
        "team",
        "match"
    )

    serializer_class = PlayerMatchStatsSerializer