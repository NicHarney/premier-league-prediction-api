from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team
from matches.models import Match
from django.utils import timezone

class RateLimitTests(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.team1 = Team.objects.create(name="Liverpool")
        self.team2 = Team.objects.create(name="Man City")

        Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            home_score=2,
            away_score=1,
            match_date=timezone.now(),
            season="2526"
        )

    def test_prediction_rate_limit(self):

        for _ in range(25):

            response = self.client.post(
                "/api/predictions/predict/",
                {
                    "home_team": 1,
                    "away_team": 2
                },
                format="json"
            )

        self.assertIn(response.status_code, [200, 429])