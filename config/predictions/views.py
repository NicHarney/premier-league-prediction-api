from django.shortcuts import render
from rest_framework import viewsets
from .models import Prediction
from .serializers import PredictionSerializer

# Create your views here.

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.select_related("match")
    serializer_class = PredictionSerializer