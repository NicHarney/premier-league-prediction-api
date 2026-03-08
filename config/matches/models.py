from django.db import models
from teams.models import Team
from .managers import PlayerMatchStatsManager
from django.utils import timezone
from django.db.models import Q, F


# Create your models here.
class Match(models.Model):
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches"
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches"
    )
    match_date = models.DateTimeField(db_index=True)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    season = models.CharField(max_length=9, db_index=True)

    expected_home_goals = models.FloatField(null=True, blank=True)
    expected_away_goals = models.FloatField(null=True, blank=True)

    ordering = ["-match_date"]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
    
    class Meta:
        indexes = [
            models.Index(fields=["season", "match_date"]),
            models.Index(fields=["home_team","match_date"]),
            models.Index(fields=["away_team","match_date"]),
        ]

class PlayerMatchStats(models.Model):

    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="match_stats",
        db_index=True
    )

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        db_index=True
    )
    match = models.ForeignKey(
        "Match",
        on_delete=models.CASCADE,
        related_name="player_stats",
        db_index=True
    )

    minutes_played = models.IntegerField()
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)

    rolling_shots_3 = models.FloatField(null=True, blank=True)
    rolling_shots_5 = models.FloatField(null=True, blank=True)
    rolling_goals_5 = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Custom manager for advanced queries
    objects = PlayerMatchStatsManager()

    class Meta:
        indexes = [
            models.Index(fields=["player", "match"]),
            models.Index(fields=["player", "team"]),
            models.Index(fields=["team", "match"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["player", "match"], name="unique_player_match_stats"),

            models.CheckConstraint(
                condition=Q(goals__gte=0),
                name="goals_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(assists__gte=0),
                name="assists_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(shots__gte=0),
                name="shots_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(shots_on_target__lte=F("shots")),
                name="shots_on_target_valid"
            ),
            models.CheckConstraint(
                condition=Q(minutes_played__gte=0, minutes_played__lte=120),
                name="valid_minutes_played"
            ),
            
            models.CheckConstraint(
                condition=Q(fouls__gte=0),
                name="fouls_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(yellow_cards__gte=0),
                name="yellow_cards_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(red_cards__gte=0),
                name="red_cards_non_negative"
            ),
        ]

    def __str__(self):
        return f"{self.player} - {self.match} stats"