from django.shortcuts import render
from rest_framework import viewsets
from .models import Match, PlayerMatchStats
from .serializers import MatchSerializer, PlayerMatchStatsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.

class MatchViewSet(viewsets.ModelViewSet):

    queryset = Match.objects.select_related(
        "home_team",
        "away_team"
    ).all()

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

    ordering = ["-match_date"]

    @action(detail=True, methods=["get"])
    def player_stats(self, request, pk=None):

        try:

            match = get_object_or_404(Match, pk=pk)

            stats = PlayerMatchStats.objects.select_related(
                "player",
                "team"
            ).filter(match=match)

            serializer = PlayerMatchStatsSerializer(stats, many=True)

            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "status": "error",
                    "message": "Unable to retrieve player stats",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlayerMatchStatsViewSet(viewsets.ModelViewSet):

    queryset = PlayerMatchStats.objects.select_related(
        "player",
        "team",
        "match"
    ).all()

    serializer_class = PlayerMatchStatsSerializer

    
    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "player",
        "team",
        "match",
    ]


    search_fields = ["player__name"]