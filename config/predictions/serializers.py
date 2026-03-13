from rest_framework import serializers
from .models import Prediction

# serializers for input validation
class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = "__all__"


class MatchPredictionSerializer(serializers.Serializer):

    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()

    def validate(self,data):
        if data["home_team"] == data["away_team"]:
            raise serializers.ValidationError(
                "Home and away teams must be different"
            )
        return data

class ValueBetSerializer(serializers.Serializer):
    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()

    # ensure realistic odds are entered
    home_odds = serializers.FloatField(min_value=1.01, max_value=100)
    draw_odds = serializers.FloatField(min_value=1.01, max_value=100)
    away_odds = serializers.FloatField(min_value=1.01, max_value=100)

    def validate(self,data):

        if data["home_team"] == data["away_team"]:
            raise serializers.ValidationError(
                "Home and away teams must be different"
            )

        if data["home_odds"] <= 1:
            raise serializers.ValidationError(
                "Odds must be greater than 1"
            )

        if data["draw_odds"] <= 1:
            raise serializers.ValidationError(
                "Odds must be greater than 1"
            )

        if data["away_odds"] <= 1:
            raise serializers.ValidationError(
                "Odds must be greater than 1"
            )
        
        return data