from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

    home_attack_strength = models.FloatField(default=1.0)
    home_defence_strength = models.FloatField(default=1.0)

    away_attack_strength = models.FloatField(default=1.0)
    away_defence_strength = models.FloatField(default=1.0)

    def __str__(self):
        return self.name