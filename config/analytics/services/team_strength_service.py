from teams.models import Team
from matches.models import Match

from analytics.services.weighting import match_weight
from django.utils import timezone

# function which calculates team strengths
def calculate_team_strengths():

    matches = Match.objects.select_related("home_team", "away_team")

    # --- calculate weighted league averages ---

    home_goals_weighted = 0
    away_goals_weighted = 0
    total_weight = 0
    prediction_date = timezone.now()
    for match in matches:

        
        weight = match_weight(match.match_date, prediction_date)

        home_goals_weighted += match.home_score * weight
        away_goals_weighted += match.away_score * weight

        total_weight += weight

    league_home_avg = home_goals_weighted / total_weight if total_weight else 1
    league_away_avg = away_goals_weighted / total_weight if total_weight else 1

    # --- calculate team strengths ---

    for team in Team.objects.all():

        home_scored = 0
        home_conceded = 0
        home_weight = 0

        away_scored = 0
        away_conceded = 0
        away_weight = 0

        home_matches = matches.filter(home_team=team)
        away_matches = matches.filter(away_team=team)

        for match in home_matches:

            weight = match_weight(match.match_date,prediction_date)

            home_scored += match.home_score * weight
            home_conceded += match.away_score * weight
            home_weight += weight

        for match in away_matches:

            weight = match_weight(match.match_date,prediction_date)

            away_scored += match.away_score * weight
            away_conceded += match.home_score * weight
            away_weight += weight

        # calculate attack/defence strengths compared to league average
        avg_home_scored = home_scored / home_weight if home_weight else 0
        avg_home_conceded = home_conceded / home_weight if home_weight else 0

        avg_away_scored = away_scored / away_weight if away_weight else 0
        avg_away_conceded = away_conceded / away_weight if away_weight else 0

        home_attack = avg_home_scored / league_home_avg if league_home_avg else 1
        home_defence = league_away_avg / avg_home_conceded if avg_home_conceded else 1

        away_attack = avg_away_scored / league_away_avg if league_away_avg else 1
        away_defence = league_home_avg / avg_away_conceded if avg_away_conceded else 1

        team.home_attack_strength = home_attack
        team.home_defence_strength = home_defence

        team.away_attack_strength = away_attack
        team.away_defence_strength = away_defence

        team.save()