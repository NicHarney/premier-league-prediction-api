from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stadium = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)

    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name