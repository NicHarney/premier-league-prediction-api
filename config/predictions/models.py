from django.db import models
from matches.models import Match

# Create your models here.
class Prediction(models.Model):

    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE
    )

    home_win_probability = models.FloatField()
    draw_probability = models.FloatField()
    away_win_probability = models.FloatField()

    predicted_home_goals = models.FloatField()
    predicted_away_goals = models.FloatField()

    model_version = models.CharField(max_length=50)