import csv
from io import StringIO
from django.core.management.base import BaseCommand
from players.models import Player
from teams.models import Team
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "players" / "data" 
class Command(BaseCommand):

    help = "Load player dataset"

    def handle(self, *args, **kwargs):

        path = Path(DATA_DIR / "players.csv")

        with open(path, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                team = Team.objects.filter(name=row["team"]).first()

                if not team:
                    continue

                Player.objects.create(
                    name=row["name"],
                    team=team,
                    position=row["position"]
                )

        self.stdout.write(self.style.SUCCESS("Players loaded"))