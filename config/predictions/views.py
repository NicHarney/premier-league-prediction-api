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



@api_view(["POST"])
def predict_match_view(request):

    try:

        home_team_id = request.data.get("home_team")
        away_team_id = request.data.get("away_team")

        if home_team_id is None or away_team_id is None:
            return Response(
                {
                    "status": "error",
                    "message": "home_team and away_team are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            home_team_id = int(home_team_id)
            away_team_id = int(away_team_id)
        except ValueError:
            return Response(
                {
                    "status": "error",
                    "message": "Team IDs must be integers"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
def value_bet_view(request):

    try:
        home_team_id = int(request.data.get("home_team"))
        away_team_id = int(request.data.get("away_team"))
    except (TypeError, ValueError):
        return Response(
            {
                "status": "error",
                "message": "Invalid team IDs"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if home_team_id == away_team_id:
        return Response(
            {
                "status": "error",
                "message": "home_team and away_team cannot be the same"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    home_team = get_object_or_404(Team, id=home_team_id)
    away_team = get_object_or_404(Team, id=away_team_id)

   

    home_odds = request.data.get("home_odds")
    draw_odds = request.data.get("draw_odds")
    away_odds = request.data.get("away_odds")

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