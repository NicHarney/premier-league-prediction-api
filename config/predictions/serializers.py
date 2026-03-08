from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = "__all__"


class MatchPredictionSerializer(serializers.Serializer):

    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()