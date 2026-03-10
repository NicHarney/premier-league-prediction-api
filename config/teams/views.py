from django.shortcuts import render
from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer


from rest_framework.decorators import action
from rest_framework.response import Response
from players.models import Player
from players.serializers import PlayerSerializer

# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"])
    def players(self, request, pk=None):

        players = Player.objects.filter(team_id=pk)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)