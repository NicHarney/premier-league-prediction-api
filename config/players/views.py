from django.shortcuts import render
from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related("team").order_by("name")
    serializer_class = PlayerSerializer


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["team"]

    search_fields = ["name", "position"]
    ordering_fields = ["name", "team"]
    ordering = ["name"]

    def get_queryset(self):

        queryset = super().get_queryset()

        position = self.request.query_params.get("position")

        if position:
            queryset = queryset.filter(position=position)
        
        return queryset