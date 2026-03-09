import math
from collections import defaultdict

from matches.models import Match
from predictions.services.poisson_model import predict_match
from predictions.services.value_bets import evaluate_match_value


DECAY_RATE = 0.002
VALUE_THRESHOLD = 0.05
STAKE = 1
MIN_MATCHES_FOR_TEAM = 5


def time_weight(match_date, current_date):

    days_old = (current_date - match_date).days
    return math.exp(-DECAY_RATE * days_old)


def compute_weighted_strengths(past_matches, current_date):

    goals_scored = defaultdict(float)
    goals_conceded = defaultdict(float)
    matches_played = defaultdict(float)

    total_home_goals = 0
    total_away_goals = 0
    total_weight = 0

    for m in past_matches:

        weight = time_weight(m.match_date, current_date)

        home = m.home_team_id
        away = m.away_team_id

        goals_scored[home] += m.home_score * weight
        goals_conceded[home] += m.away_score * weight

        goals_scored[away] += m.away_score * weight
        goals_conceded[away] += m.home_score * weight

        matches_played[home] += weight
        matches_played[away] += weight

        total_home_goals += m.home_score * weight
        total_away_goals += m.away_score * weight
        total_weight += weight

    if total_weight == 0:
        return None

    league_home_avg = total_home_goals / total_weight
    league_away_avg = total_away_goals / total_weight

    return goals_scored, goals_conceded, matches_played, league_home_avg, league_away_avg


def is_bet_winner(outcome, match):

    total_goals = match.home_score + match.away_score

    if outcome == "home_win":
        return match.home_score > match.away_score

    if outcome == "away_win":
        return match.home_score < match.away_score

    if outcome == "draw":
        return match.home_score == match.away_score

    if outcome == "over_2_5":
        return total_goals > 2

    if outcome == "under_2_5":
        return total_goals <= 2

    return False


def run_backtest():

    matches = Match.objects.select_related(
        "home_team",
        "away_team",
        "odds"
    ).order_by("match_date")

    past_matches = []

    bets_placed = 0
    wins = 0
    profit = 0
    matches_tested = 0

    for match in matches:

        strengths = compute_weighted_strengths(past_matches, match.match_date)

        if strengths is None:
            past_matches.append(match)
            continue

        goals_scored, goals_conceded, matches_played, league_home_avg, league_away_avg = strengths

        home_id = match.home_team_id
        away_id = match.away_team_id

        if (
            matches_played[home_id] < MIN_MATCHES_FOR_TEAM or
            matches_played[away_id] < MIN_MATCHES_FOR_TEAM
        ):
            past_matches.append(match)
            continue

        home_attack = (
            goals_scored[home_id] /
            matches_played[home_id]
        ) / league_home_avg

        home_defence = (
            league_away_avg /
            (goals_conceded[home_id] / matches_played[home_id])
        )

        away_attack = (
            goals_scored[away_id] /
            matches_played[away_id]
        ) / league_home_avg

        away_defence = (
            league_away_avg /
            (goals_conceded[away_id] / matches_played[away_id])
        )

        home_xg = home_attack * away_defence * league_home_avg
        away_xg = away_attack * home_defence * league_away_avg

        predictions = predict_match(home_xg, away_xg)

        odds = {
            "home_win": match.odds.home_win_odds if match.odds else None,
            "draw": match.odds.draw_odds if match.odds else None,
            "away_win": match.odds.away_win_odds if match.odds else None,
            "over_2_5": match.odds.over_2_5_odds if match.odds else None,
            "under_2_5": match.odds.under_2_5_odds if match.odds else None
        }

        value = evaluate_match_value(predictions, odds)

        best_outcome = None
        best_value = 0

        for outcome in ["home_win", "draw", "away_win", "over_2_5", "under_2_5"]:

            if value[outcome] is None:
                continue

            if value[outcome]["value"] > best_value:
                best_value = value[outcome]["value"]
                best_outcome = outcome

        if best_outcome and best_value > VALUE_THRESHOLD:

            bets_placed += 1

            if is_bet_winner(best_outcome, match):

                wins += 1
                profit += odds[best_outcome] - STAKE

            else:
                profit -= STAKE

        matches_tested += 1

        past_matches.append(match)

    roi = profit / bets_placed if bets_placed else 0

    return {
        "matches_tested": matches_tested,
        "bets_placed": bets_placed,
        "wins": wins,
        "profit": round(profit, 2),
        "roi": round(roi, 3)
    }