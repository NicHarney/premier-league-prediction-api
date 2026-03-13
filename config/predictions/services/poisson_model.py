import numpy as np
from scipy.stats import poisson
import math
from predictions.services.dixon_coles import dixon_coles_adjustment

MAX_GOALS = 10

# Use poisson distribution to predict match outcomes
def predict_match(home_xg, away_xg):

    # matrix of scoreline probabilities
    score_matrix = np.zeros((MAX_GOALS, MAX_GOALS))

    for h in range(MAX_GOALS):
        for a in range(MAX_GOALS):

            base_prob = poisson.pmf(h, home_xg) * poisson.pmf(a, away_xg)
            adjustment = dixon_coles_adjustment(h, a, home_xg, away_xg)
            score_matrix[h, a] = base_prob * adjustment

    # normalize 
    score_matrix /= score_matrix.sum()

    # match outcomes
    home_win = 0
    draw = 0
    away_win = 0

    over_2_5 = 0
    under_2_5 = 0

    scorelines = []

    for h in range(MAX_GOALS):
        for a in range(MAX_GOALS):

            prob = score_matrix[h, a]

            if h > a:
                home_win += prob
            elif h == a:
                draw += prob
            else:
                away_win += prob

            if h + a > 2:
                over_2_5 += prob
            else:
                under_2_5 += prob

            scorelines.append({
                "score": f"{h}-{a}",
                "probability": float(prob)
            })

    # sort scorelines
    scorelines = sorted(
        scorelines,
        key=lambda x: x["probability"],
        reverse=True
    )

    return {
        "home_win": float(home_win),
        "draw": float(draw),
        "away_win": float(away_win),
        "over_2_5": float(over_2_5),
        "under_2_5": float(under_2_5),
        "scoreline_probabilities": scorelines[:10]
    }

