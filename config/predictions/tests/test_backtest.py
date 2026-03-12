from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team
from matches.models import Match
from django.utils import timezone

class BacktestTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.team1 = Team.objects.create(name="Arsenal")
        self.team2 = Team.objects.create(name="Chelsea")

        self.match = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            home_score=2,
            away_score=1,
            match_date=timezone.now(),
            season="2526"
        )


    def test_backtest_endpoint_runs(self):

        response = self.client.get("/api/predictions/backtest/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("roi", data["data"])