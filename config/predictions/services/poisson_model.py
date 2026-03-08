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

    over_2_5 = 0
    under_2_5 = 0

    scorelines = []

    for home_goals in range(MAX_GOALS):
        for away_goals in range(MAX_GOALS):

            prob = (
                home_goal_probs[home_goals] *
                away_goal_probs[away_goals]
            )

            total_goals = home_goals + away_goals
            scorelines.append({
                "score": f"{home_goals}-{away_goals}",
                "probability": round(prob, 4)
            })
            

            if home_goals > away_goals:
                home_win += prob
            elif home_goals == away_goals:
                draw += prob
            else:
                away_win += prob

            if total_goals > 2:
                over_2_5 += prob
            else:
                under_2_5 += prob

    # sort scorelines by probability
    scorelines = sorted(
        scorelines,
        key=lambda x: x["probability"],
        reverse=True

    )
    
    
    return {
        "home_win_probability": round(home_win, 4),
        "draw_probability": round(draw, 4),
        "away_win_probability": round(away_win, 4),
        "over_2_5_goals": round(over_2_5, 4),
        "under_2_5_goals": round(under_2_5, 4),
        "scoreline_probabilities": scorelines[:10]  
    }

