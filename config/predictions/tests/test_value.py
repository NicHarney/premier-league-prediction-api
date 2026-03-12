from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team
from matches.models import Match
from django.utils import timezone
from predictions.services.value_bets import expected_value
from predictions.services.value_bets import evaluate_markets

class ValueBetTests(TestCase):

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


    def test_value_endpoint_success(self):

        response = self.client.post(
            "/api/predictions/value/",
            {
                "home_team": self.team1.id,
                "away_team": self.team2.id,
                "home_odds": 2.5,
                "draw_odds": 3.2,
                "away_odds": 2.8
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("markets", response.data["data"])


    def test_invalid_odds_rejected(self):

        response = self.client.post(
            "/api/predictions/value/",
            {
                "home_team": self.team1.id,
                "away_team": self.team2.id,
                "home_odds": 1,
                "draw_odds": 3,
                "away_odds": 2
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

class ValueBetMathTests(TestCase):

    def test_expected_value_calculation(self):

        ev = expected_value(0.5,2.2)

        self.assertAlmostEqual(ev,0.1,places=2)

    def test_positive_ev_market_detected(self):

        predictions = {
            "home_win": 0.6,
            "draw": 0.2,
            "away_win": 0.2
        }

        odds = {
            "home_win": 2.2,
            "draw": 3.0,
            "away_win": 4.0
        }

        

        markets = evaluate_markets(predictions, odds)

        self.assertGreater(markets["home_win"]["ev"], 0)