from django.shortcuts import render
from rest_framework import viewsets
from .models import Match, PlayerMatchStats
from .serializers import MatchSerializer, PlayerMatchStatsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related(
        "home_team",
        "away_team"
    )

    serializer_class = MatchSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "season",
        "home_team",
        "away_team",
    ]

    ordering_fields = ["match_date"]

    @action(detail=True, methods=["get"])
    def player_stats(self, request, pk=None):

        stats = PlayerMatchStats.objects.filter(match_id=pk)
        serializer = PlayerMatchStatsSerializer(stats, many=True)
        return Response(serializer.data)


class PlayerMatchStatsViewSet(viewsets.ModelViewSet):

    queryset = PlayerMatchStats.objects.select_related(
        "player",
        "team",
        "match"
    )

    serializer_class = PlayerMatchStatsSerializer

    filterset_fields = [
        "player",
        "team",
        "match",
    ]