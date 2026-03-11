from django.shortcuts import render
from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related("team").all()
    serializer_class = PlayerSerializer


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["team", "position"]

    search_fields = ["name"]
    ordering_fields = ["name", "team"]
    ordering = ["name"]