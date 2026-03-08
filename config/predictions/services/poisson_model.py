import numpy as np
from scipy.stats import poisson


MAX_GOALS = 10


def predict_match(home_expected_goals, away_expected_goals):

    home_goal_probs = [
        poisson.pmf(i, home_expected_goals)
        for i in range(MAX_GOALS)
    ]

    away_goal_probs = [
        poisson.pmf(i, away_expected_goals)
        for i in range(MAX_GOALS)
    ]

    home_win = 0
    draw = 0
    away_win = 0

    score_matrix = {}

    for home_goals in range(MAX_GOALS):
        for away_goals in range(MAX_GOALS):

            prob = (
                home_goal_probs[home_goals] *
                away_goal_probs[away_goals]
            )

            score = f"{home_goals}-{away_goals}"
            score_matrix[score] = prob

            if home_goals > away_goals:
                home_win += prob
            elif home_goals == away_goals:
                draw += prob
            else:
                away_win += prob

    
    return {
        "home_win_probability": home_win,
        "draw_probability": draw,
        "away_win_probability": away_win,
        "scoreline_probabilities": score_matrix
    }

def expected_goals(home_team,away_team,league_home_avg,league_away_avg):

    home_goals = (
        home_team.home_attack_strength *
        away_team.away_defence_strength *
        league_home_avg
    )

    away_goals = (
        away_team.away_attack_strength *
        home_team.home_defence_strength *
        league_away_avg
    )

    return home_goals, away_goals