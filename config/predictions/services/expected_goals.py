HOME_ADVANTAGE = 1.1 

# calculate expected goals for each team in a game with home advantage applied
def calculate_expected_goals(home_team, away_team, league_home_avg, league_away_avg):

    home_xg = (
        home_team.home_attack_strength *
        away_team.away_defence_strength *
        league_home_avg * HOME_ADVANTAGE
    )

    away_xg = (
        away_team.away_attack_strength *
        home_team.home_defence_strength *
        league_away_avg
    )

    return home_xg, away_xg