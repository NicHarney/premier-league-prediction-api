from django.shortcuts import render
from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from players.models import Player
from players.serializers import PlayerSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by("name")
    serializer_class = TeamSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['id', 'name']
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"])
    def players(self, request, pk=None):

        try:
            team = get_object_or_404(Team, id=pk)
            players = Player.objects.filter(current_team=team)
            serializer = PlayerSerializer(players, many=True)
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
                    "message": "Unable to retrieve players for the specified team."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )