from rest_framework import serializers
from .models import Match, PlayerMatchStats

# serializers to validate user input
class MatchSerializer(serializers.ModelSerializer):

    home_team_name = serializers.CharField(
        source="home_team.name",
        read_only=True
    )

    away_team_name = serializers.CharField(
        source="away_team.name",
        read_only=True
    )

    class Meta:
        model = Match
        fields = "__all__"

class PlayerMatchStatsSerializer(serializers.ModelSerializer):

    player_name = serializers.CharField(
        source="player.name",
        read_only=True
    )

    class Meta:
        model = PlayerMatchStats
        fields = "__all__"