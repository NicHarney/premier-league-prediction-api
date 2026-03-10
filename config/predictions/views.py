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



@api_view(["POST"])
def predict_match_view(request):

    try:
        home_team_id = int(request.data.get("home_team"))
        away_team_id = int(request.data.get("away_team"))
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid team IDs"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    home_team = Team.objects.get(id=home_team_id)
    away_team = Team.objects.get(id=away_team_id)

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

    return Response(
        {
            "home_team": home_team.name,
            "away_team": away_team.name,
            "home_xg": home_xg,
            "away_xg": away_xg,
            "predictions": predictions,
        }
    )


@api_view(["POST"])
def value_bet_view(request):

    try:
        home_team_id = int(request.data.get("home_team"))
        away_team_id = int(request.data.get("away_team"))
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid team IDs"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    home_team = Team.objects.get(id=home_team_id)
    away_team = Team.objects.get(id=away_team_id)

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

    odds = request.data.get("odds")

    if not odds:
        return Response(
            {"error": "Odds must be provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    predictions = predict_match(home_xg, away_xg)

    markets = evaluate_markets(predictions, odds)

    return Response(
        {
            "predictions": predictions,
            "markets": markets,
        }
    )


@api_view(["GET"])
def backtest_view(request):

    matches = Match.objects.select_related("odds").all()

    results = run_backtest(matches)

    return Response(results)