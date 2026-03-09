from matches.models import Match
from teams.models import Team
from django.db.models import Avg

from predictions.services.expected_goals import calculate_expected_goals
from predictions.services.poisson_model import predict_match
from predictions.services.value_bets import evaluate_match_value

STAKE = 1

def run_backtest():

    matches = Match.objects.select_related(
        "home_team",
        "away_team",
        "odds"
    ).exclude(
        odds__home_win_odds__isnull=True,
    )

    league_home_avg = Match.objects.aggregate(avg=Avg("home_score"))["avg"]
    league_away_avg = Match.objects.aggregate(avg=Avg("away_score"))["avg"]

    bets_placed = 0
    wins = 0
    profit = 0

    for match in matches:
        home_team = match.home_team
        away_team = match.away_team

        home_xg, away_xg = calculate_expected_goals(
            home_team,
            away_team,
            league_home_avg,
            league_away_avg
        )

        predictions = predict_match(home_xg, away_xg)

        betting_odds = {
            "home_win": match.odds.home_win_odds,
            "draw": match.odds.draw_odds,
            "away_win": match.odds.away_win_odds
        }
        value = evaluate_match_value(predictions, betting_odds)

        for outcome in ["home_win", "draw", "away_win"]:
            if value[outcome]["value"] > 0.05:
                bets_placed += 1
                actual_result = get_match_result(match)
                if outcome == actual_result:
                    wins += 1
                    profit += betting_odds[outcome] - 1
                else:
                    profit -= 1
    
    roi =profit / bets_placed if bets_placed > 0 else 0

    return {
        "matches_tested": matches.count(),
        "bets_placed": bets_placed,
        "wins": wins,
        "profit": round(profit, 2),
        "roi": round(roi, 2)
    }

def get_match_result(match):

    if match.home_score > match.away_score:
        return "home_win"
    elif match.home_score == match.away_score:
        return "draw"
    else:
        return "away_win"
                