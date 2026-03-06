from django.db import models
from matches.models import Match

# Create your models here.
class BettingOdds(models.Model):

    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE
    )

    home_win_odds = models.FloatField()
    draw_odds = models.FloatField()
    away_win_odds = models.FloatField()

    bookmaker = models.CharField(max_length=100)