from django.db import models
from matches.models import Match

# Create your models here.
class BettingOdds(models.Model):

    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="odds"
    )

    home_win_odds = models.FloatField()
    draw_odds = models.FloatField()
    away_win_odds = models.FloatField()

    over_2_5_odds = models.FloatField(null=True)
    under_2_5_odds = models.FloatField(null=True)

    bookmaker = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f"Odds for {self.match}"

    class Meta:
        indexes = [
            models.Index(fields=["bookmaker"]),
        ]

class LeagueStatistics(models.Model):

    season = models.CharField(max_length=9, unique=True, db_index=True)
    average_home_goals = models.FloatField()
    average_away_goals = models.FloatField()

    updated_at = models.DateTimeField(auto_now=True)