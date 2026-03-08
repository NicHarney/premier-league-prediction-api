import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from teams.models import Team
from matches.models import Match
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data" / "seasons"


class Command(BaseCommand):

    help = "Load Premier League datasets"

    def handle(self, *args, **kwargs):

        self.stdout.write("Loading football datasets...")

        self.stdout.write(f"Looking for CSV files in {DATA_DIR}")

        for csv_file in DATA_DIR.glob("*.csv"):

            season = csv_file.stem

            self.stdout.write(f"Processing season {season}")

            with open(csv_file, encoding="utf-8") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    home_team, _ = Team.objects.get_or_create(
                        name=row["HomeTeam"]
                    )

                    away_team, _ = Team.objects.get_or_create(
                        name=row["AwayTeam"]
                    )

                    date = row["Date"]
                    try:
                        match_date = datetime.strptime(row["Date"], "%d/%m/%y")
                    except ValueError:
                        match_date = datetime.strptime(row["Date"], "%d/%m/%Y")
                    Match.objects.get_or_create(
                        home_team=home_team,
                        away_team=away_team,
                        match_date=match_date,
                        season=season,
                        home_score=int(row["FTHG"]),
                        away_score=int(row["FTAG"])
                    )

        self.stdout.write(self.style.SUCCESS("Dataset loaded"))