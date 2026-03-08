import csv
import requests
from io import StringIO
from pathlib import Path

from django.core.management.base import BaseCommand

from teams.models import Team
from matches.models import Match
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data" / "seasons"


SEASONS = [
    "2526",
    "2425",
    "2324",
    "2223",
    "2122",
    "2021",
    "1920",
    "1819",
    "1718",
    "1617",
    "1516",
]

class Command(BaseCommand):

    help = "Load Premier League datasets"

    def handle(self, *args, **kwargs):

        self.stdout.write("Loading football datasets...")

        self.stdout.write(f"Looking for CSV files in {DATA_DIR}")

        for season in SEASONS:
            url = f"https://www.football-data.co.uk/mmz4281/{season}/E0.csv"

            self.stdout.write(f"Downloading season {season}")

            response = requests.get(url)

            csv_file = StringIO(response.text)

            reader = csv.DictReader(csv_file)

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
                    defaults={
                        "season": season,
                        "home_score": int(row["FTHG"]),
                        "away_score": int(row["FTAG"])
                    }
                    
                )

        self.stdout.write(self.style.SUCCESS("Dataset loaded"))