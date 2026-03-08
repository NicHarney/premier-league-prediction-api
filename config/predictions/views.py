from django.shortcuts import render
from rest_framework import viewsets
from .models import Prediction
from .serializers import PredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from teams.models import Team
from matches.models import Match

from predictions.serializers import MatchPredictionSerializer
from predictions.services.poisson_model import predict_match, expected_goals

from django.db.models import Avg

# Create your views here.

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.select_related("match")
    serializer_class = PredictionSerializer


class MatchPredictionView(APIView):

    def post(self, request):
        serializer = MatchPredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        home_team = Team.objects.get(id=serializer.validated_data["home_team"])
        away_team = Team.objects.get(id=serializer.validated_data["away_team"])

        league_home_avg = Match.objects.aggregate(avg=Avg("home_score"))["avg"]
        league_away_avg = Match.objects.aggregate(avg=Avg("away_score"))["avg"]

        home_xg, away_xg = expected_goals(
            home_team,
            away_team,
            league_home_avg,
            league_away_avg
        )

        probabilities = predict_match(home_xg, away_xg)
        return Response({
            "home_team": home_team.name,
            "away_team": away_team.name,
            "expected_home_goals": home_xg,
            "expected_away_goals": away_xg,
            **probabilities,
        })