from django.db import models
from teams.models import Team

# Create your models here.
class Player(models.Model):
  

    name = models.CharField(max_length=100, db_index=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="players"
    )

    position = models.CharField(max_length=50, db_index=True)

    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name