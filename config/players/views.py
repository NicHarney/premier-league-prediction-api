from django.shortcuts import render
from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related("team")
    serializer_class = PlayerSerializer

    filterset_fields = ["team", "position"]