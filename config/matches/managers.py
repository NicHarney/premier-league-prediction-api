from django.db import models

class PlayerMatchQuerySet(models.QuerySet):
    def for_player(self, player_id):
        return self.filter(player_id=player_id)

    def last_n_matches(self, player_id):
        return (
            self.filter(player_id=player_id)
            .order_by("-match_date")[:n]
        )

    def high_shot_players(self):
        return self.filter(rolling_shots_5__gte=3)

class PlayerMatchStatsManager(models.Manager):
    def get_queryset(self):
        return PlayerMatchQuerySet(self.model, using=self._db)

    def recent_form(self, player_id):
        return self.get_queryset().last_n_matches(player_id, 5)