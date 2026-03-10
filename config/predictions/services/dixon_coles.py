import math

RHO = -0.1  # typical value from research papers


def dixon_coles_adjustment(home_goals, away_goals, home_xg, away_xg):

    if home_goals == 0 and away_goals == 0:
        return 1 - (home_xg * away_xg * RHO)

    if home_goals == 0 and away_goals == 1:
        return 1 + (home_xg * RHO)

    if home_goals == 1 and away_goals == 0:
        return 1 + (away_xg * RHO)

    if home_goals == 1 and away_goals == 1:
        return 1 - RHO

    return 1