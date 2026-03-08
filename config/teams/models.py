from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stadium = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)

    founded_year = models.IntegerField(null=True, blank=True)

    # statistical fields
    average_goals_scored = models.FloatField(default=0.0)
    average_goals_conceded = models.FloatField(default=0.0)

    home_attack_strength = models.FloatField(default=1.0)
    home_defence_strength = models.FloatField(default=1.0)

    away_attack_strength = models.FloatField(default=1.0)
    away_defence_strength = models.FloatField(default=1.0)

    def __str__(self):
        return self.name