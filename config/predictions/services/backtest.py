from collections import defaultdict

from predictions.services.poisson_model import predict_match
from predictions.services.value_bets import evaluate_markets
from predictions.services.expected_goals import calculate_expected_goals
from analytics.services.weighting import match_weight


EDGE_THRESHOLD = 0.12
MIN_ODDS = 1.7


def run_backtest(matches):

    matches = matches.order_by("match_date")

    goals_scored = defaultdict(int)
    goals_conceded = defaultdict(int)
    matches_played = defaultdict(int)

    total_home_goals = 0
    total_away_goals = 0
    total_matches = 0

    bets = 0
    wins = 0
    profit = 0

    for match in matches:

        home_id = match.home_team_id
        away_id = match.away_team_id

       
        # Skip early matches where we have no historical data
        if matches_played[home_id] < 5 or matches_played[away_id] < 5:

            update_team_stats(match, match.match_date, goals_scored, goals_conceded, matches_played)

            total_home_goals += match.home_score
            total_away_goals += match.away_score
            total_matches += 1

            continue

        
        league_home_avg = total_home_goals / total_matches
        league_away_avg = total_away_goals / total_matches

       

        home_xg, away_xg = calculate_expected_goals(
            match.home_team,
            match.away_team,
            league_home_avg,
            league_away_avg
        )

        predictions = predict_match(home_xg, away_xg)

        odds = {
            "home_win": match.odds.home_win_odds if match.odds else None,
            "draw": match.odds.draw_odds if match.odds else None,
            "away_win": match.odds.away_win_odds if match.odds else None,
            "over_2_5": match.odds.over_2_5_odds if match.odds else None,
            "under_2_5": match.odds.under_2_5_odds if match.odds else None
        }

        markets = evaluate_markets(predictions, odds)

        best_market = None
        best_ev = 0

        best_market = None
        best_edge = 0

        for market, data in markets.items():
            
          
            if data["odds"] is None:
                continue


            if market not in ["home_win", "draw", "away_win"]:
                continue
            if data["odds"] < MIN_ODDS:
                continue

            if data["probability"] > 0.7 or data["probability"] < 0.15:
                continue

            if data["edge"] > best_edge:
                best_edge = data["edge"]
                best_market = market


        if best_market and best_edge > EDGE_THRESHOLD:

            bets += 1

            if bet_wins(best_market, match):
                wins += 1
                profit += odds[best_market] - 1
            else:
                profit -= 1

        update_team_stats(match, match.match_date, goals_scored, goals_conceded, matches_played)

        total_home_goals += match.home_score
        total_away_goals += match.away_score
        total_matches += 1

    roi = profit / bets if bets else 0

    return {
        "bets": bets,
        "wins": wins,
        "profit": round(profit, 2),
        "roi": round(roi, 3)
    }

def update_team_stats(match, prediction_date, goals_scored, goals_conceded, matches_played):

    weight = match_weight(match.match_date, prediction_date)

    home = match.home_team_id
    away = match.away_team_id

    goals_scored[home] += match.home_score * weight
    goals_conceded[home] += match.away_score * weight

    goals_scored[away] += match.away_score * weight
    goals_conceded[away] += match.home_score * weight

    matches_played[home] += weight
    matches_played[away] += weight

def bet_wins(market, match):

    if market == "home_win":
        return match.home_score > match.away_score

    if market == "away_win":
        return match.away_score > match.home_score

    if market == "draw":
        return match.home_score == match.away_score

    if market == "over_2_5":
        return (match.home_score + match.away_score) > 2

    if market == "under_2_5":
        return (match.home_score + match.away_score) <= 2

    return False