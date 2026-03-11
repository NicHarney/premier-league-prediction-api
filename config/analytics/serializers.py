from rest_framework import serializers
from .models import BettingOdds


class BettingOddsSerializer(serializers.ModelSerializer):

    home_team = serializers.CharField(
        source="match.home_team.name",
        read_only=True
    )

    away_team = serializers.CharField(
        source="match.away_team.name",
        read_only=True
    )

    match_date = serializers.DateTimeField(
        source="match.match_date",
        read_only=True
    )

    class Meta:
        model = BettingOdds
        fields = [
            "id",
            "match",
            "home_team",
            "away_team",
            "match_date",
            "home_win_odds",
            "draw_odds",
            "away_win_odds",
            "bookmaker",
        ]