from matches.models import Match
from teams.models import Team
from django.db.models import Avg

from predictions.services.expected_goals import calculate_expected_goals
from predictions.services.poisson_model import predict_match
from predictions.services.value_bets import evaluate_match_value

from collections import defaultdict

STAKE = 1
VALUE_THRESHOLD = 0.05
MIN_MATCHES_FOR_TEAM = 5


def run_backtest():

    matches = Match.objects.select_related(
        "home_team",
        "away_team",
        "odds"
    ).exclude(
        odds__home_win_odds__isnull=True
    ).order_by("match_date")

    goals_scored = defaultdict(int)
    goals_conceded = defaultdict(int)
    matches_played = defaultdict(int)

    total_home_goals = 0
    total_away_goals = 0
    total_matches = 0

    bets_placed = 0
    wins = 0
    profit = 0

    matches_tested = 0

    for match in matches:

        # Skip prediction if we have no prior data
        if total_matches < 50:
            update_team_stats(
                match,
                goals_scored,
                goals_conceded,
                matches_played
            )

            total_home_goals += match.home_score
            total_away_goals += match.away_score
            total_matches += 1

            continue

        league_home_avg = total_home_goals / total_matches
        league_away_avg = total_away_goals / total_matches

        home_id = match.home_team_id
        away_id = match.away_team_id

        if (matches_played[home_id] < MIN_MATCHES_FOR_TEAM) or (matches_played[away_id] < MIN_MATCHES_FOR_TEAM):

            update_team_stats(
                match,
                goals_scored,
                goals_conceded,
                matches_played
            )

            total_home_goals += match.home_score
            total_away_goals += match.away_score
            total_matches += 1

            continue

        avg_scored_home = goals_scored[home_id] / matches_played[home_id]
        avg_conceded_home = goals_conceded[home_id] / matches_played[home_id]

        avg_scored_away = goals_scored[away_id] / matches_played[away_id]
        avg_conceded_away = goals_conceded[away_id] / matches_played[away_id]

        # Prevent divide-by-zero when a team has conceded 0 goals
        if avg_conceded_home == 0:
            avg_conceded_home = 0.01

        if avg_conceded_away == 0:
            avg_conceded_away = 0.01


        home_attack = avg_scored_home / league_home_avg
        home_defence = league_away_avg / avg_conceded_home

        away_attack = avg_scored_away / league_home_avg
        away_defence = league_away_avg / avg_conceded_away

        home_xg = home_attack * away_defence * league_home_avg
        away_xg = away_attack * home_defence * league_away_avg

        predictions = predict_match(home_xg, away_xg)

        odds = {
            "home_win": match.odds.home_win_odds,
            "draw": match.odds.draw_odds,
            "away_win": match.odds.away_win_odds
        }

        value = evaluate_match_value(predictions, odds)

        actual_result = get_match_result(match)

        for outcome in ["home_win", "draw", "away_win"]:

            if value[outcome]["value"] > VALUE_THRESHOLD:

                bets_placed += 1

                if outcome == actual_result:

                    wins += 1
                    profit += odds[outcome] - STAKE

                else:

                    profit -= STAKE

        matches_tested += 1

        update_team_stats(
            match,
            goals_scored,
            goals_conceded,
            matches_played
        )

        total_home_goals += match.home_score
        total_away_goals += match.away_score
        total_matches += 1

    roi = profit / bets_placed if bets_placed else 0

    return {
        "matches_tested": matches_tested,
        "bets_placed": bets_placed,
        "wins": wins,
        "profit": round(profit, 2),
        "roi": round(roi, 3)
    }


def update_team_stats(match, goals_scored, goals_conceded, matches_played):

    home = match.home_team_id
    away = match.away_team_id

    goals_scored[home] += match.home_score
    goals_conceded[home] += match.away_score

    goals_scored[away] += match.away_score
    goals_conceded[away] += match.home_score

    matches_played[home] += 1
    matches_played[away] += 1


def get_match_result(match):

    if match.home_score > match.away_score:
        return "home_win"

    if match.home_score < match.away_score:
        return "away_win"

    return "draw"