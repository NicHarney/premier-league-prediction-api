import random
from django.core.management.base import BaseCommand
from players.models import Player
from matches.models import Match, PlayerMatchStats

# Generate sample player stats for players that exist in the database
class Command(BaseCommand):

    help = "Generate example player match stats"

    def handle(self, *args, **kwargs):

        players = Player.objects.all()
        matches = Match.objects.all()

        created = 0

        for player in players:

            # give each player stats for 3 matches
            sample_matches = matches.order_by("?")[:3]

            for match in sample_matches:

                if PlayerMatchStats.objects.filter(
                    player=player,
                    match=match
                ).exists():
                    continue

                shots = random.randint(0,5)

                PlayerMatchStats.objects.create(

                    player=player,
                    team=player.team,
                    match=match,

                    minutes_played=random.randint(10,90),

                    goals=random.randint(0,2),
                    assists=random.randint(0,1),

                    shots=shots,
                    shots_on_target=random.randint(0,shots),

                    fouls=random.randint(0,3),
                    yellow_cards=random.randint(0,1),
                    red_cards=0

                )

                created += 1

        print(f"Created {created} player match stat rows")