from django.db import models
from teams.models import Team

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
        on_delete=models.CASCADE
    )

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    minutes_played = models.IntegerField()
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["player", "match"])
        ]
        constraints = [
            models.UniqueConstraint(fields=["player", "match"], name="unique_player_match_stats")
        ]