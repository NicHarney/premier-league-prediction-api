from teams.models import Team
from matches.models import Match

from analytics.services.weighting import match_weight


def calculate_team_strengths():

    matches = Match.objects.all()

    # --- calculate weighted league average goals ---

    weighted_goals = 0
    total_weight = 0

    for match in matches:

        weight = match_weight(match.match_date)

        weighted_goals += match.home_score * weight
        weighted_goals += match.away_score * weight

        # two goal observations per match
        total_weight += 2 * weight

    league_avg_goals = weighted_goals / total_weight if total_weight else 1

    # --- calculate team strengths ---

    for team in Team.objects.all():

        scored_weighted = 0
        conceded_weighted = 0
        team_weight = 0

        team_matches = matches.filter(home_team=team) | matches.filter(away_team=team)

        for match in team_matches:

            weight = match_weight(match.match_date)

            if match.home_team == team:

                goals_scored = match.home_score
                goals_conceded = match.away_score

            else:

                goals_scored = match.away_score
                goals_conceded = match.home_score

            scored_weighted += goals_scored * weight
            conceded_weighted += goals_conceded * weight

            team_weight += weight

        avg_scored = scored_weighted / team_weight if team_weight else 0
        avg_conceded = conceded_weighted / team_weight if team_weight else 0

        attack_strength = avg_scored / league_avg_goals if league_avg_goals else 1
        defence_strength = league_avg_goals / avg_conceded  if avg_conceded else 1

        team.avg_goals_scored = avg_scored
        team.avg_goals_conceded = avg_conceded
        team.attack_strength = attack_strength
        team.defence_strength = defence_strength

        team.save()