from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg
from matches.models import Match
from predictions.services.poisson_model import predict_match
from predictions.services.value_bets import evaluate_markets
from predictions.services.backtest import run_backtest
from teams.models import Team
from predictions.services.expected_goals import calculate_expected_goals
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .throttles import PredictionThrottle, BacktestThrottle
from rest_framework.decorators import throttle_classes
from .serializers import MatchPredictionSerializer, ValueBetSerializer



@api_view(["POST"])
@throttle_classes([PredictionThrottle])
def predict_match_view(request):

    
    try:

        serializer = MatchPredictionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        home_team_id = serializer.validated_data["home_team"]
        away_team_id = serializer.validated_data["away_team"]

     

        
        #home_team_id = int(home_team_id)
        #away_team_id = int(away_team_id)
   

        home_team = get_object_or_404(Team, id=home_team_id)
        away_team = get_object_or_404(Team, id=away_team_id)

        stats = Match.objects.aggregate(
            home_avg=Avg("home_score"),
            away_avg=Avg("away_score"),
        )

        league_home_avg = stats["home_avg"]
        league_away_avg = stats["away_avg"]

        if league_home_avg is None or league_away_avg is None:
            return Response(
                {
                    "status": "error",
                    "message": "Insufficient match data to calculate league averages"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        home_xg, away_xg = calculate_expected_goals(
            home_team,
            away_team,
            league_home_avg,
            league_away_avg
        )

        predictions = predict_match(home_xg, away_xg)

        return Response(
            {
                "status": "success",
                "data": {
                    "teams": {
                        "home": home_team.name,
                        "away": away_team.name
                    },
                    "expected_goals": {
                        "home": round(home_xg, 2),
                        "away": round(away_xg, 2)
                    },
                    "probabilities": {
                        "home_win": round(predictions["home_win"], 2),
                        "draw": round(predictions["draw"], 2),
                        "away_win": round(predictions["away_win"], 2)
                    },
                    "totals": {
                        "over_2_5": round(predictions["over_2_5"], 2),
                        "under_2_5": round(predictions["under_2_5"], 2)
                    },
                    "top_scorelines": predictions["scoreline_probabilities"]
                }
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:

        return Response(
            {
                "status": "error",
                "message": "Prediction failed",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@throttle_classes([PredictionThrottle])
def value_bet_view(request):
  
    serializer = ValueBetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    home_team_id = serializer.validated_data["home_team"]
    away_team_id = serializer.validated_data["away_team"]

    home_team = get_object_or_404(Team, id=home_team_id)
    away_team = get_object_or_404(Team, id=away_team_id)

   

    home_odds = serializer.validated_data["home_odds"]
    draw_odds = serializer.validated_data["draw_odds"]
    away_odds = serializer.validated_data["away_odds"]

    if not home_odds or not draw_odds or not away_odds:
        return Response(
            {
                "status": "error",
                "message": "Missing odds for one or more outcomes"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        odds = {
            "home_win": float(home_odds),
            "draw": float(draw_odds),
            "away_win": float(away_odds),
        }
    except ValueError:
        return Response(
            {
                "status": "error",
                "message": "Invalid odds format"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


    try:
        league_home_avg = Match.objects.aggregate(
            Avg("home_score")
        )["home_score__avg"]

        league_away_avg = Match.objects.aggregate(
            Avg("away_score")
        )["away_score__avg"]

        home_xg, away_xg = calculate_expected_goals(
            home_team,
            away_team,
            league_home_avg,
            league_away_avg
        )
        predictions = predict_match(home_xg, away_xg)

        markets = evaluate_markets(predictions, odds)

        return Response(
            {
                "status": "success",
                "data": {
                    "predictions": predictions,
                    "markets": markets,
                }
            }
        )
    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": "Internal server error",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@throttle_classes([BacktestThrottle])
def backtest_view(request):

    try:

        matches = Match.objects.select_related("odds").all()

        if not matches.exists():
            return Response(
                {
                    "status": "error",
                    "message": "No matches available for backtesting"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        results = run_backtest(matches)
        return Response(
            {
                "status": "success",
                "data": results
            },
            status=status.HTTP_200_OK,
        )
    
    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": "Internal server error",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def frontend_view(request):
    return render(request, "index.html")