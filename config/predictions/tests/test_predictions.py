from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team
from matches.models import Match
from django.utils import timezone
from predictions.services.poisson_model import predict_match

class PredictEndpointTests(TestCase):

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


    def test_predict_match_success(self):

        response = self.client.post(
            "/api/predictions/predict/",
            {
                "home_team": self.team1.id,
                "away_team": self.team2.id
            },
            format="json"
        )


        
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("probabilities", data["data"])

        

    def test_predict_same_team_error(self):

        response = self.client.post(
            "/api/predictions/predict/",
            {
                "home_team": self.team1.id,
                "away_team": self.team1.id
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_predict_invalid_team(self):

        response = self.client.post(
            "api/predictions/predict/",
            {
                "home_team": 999,
                "away_team": 888
            },

            format="json"

        )

        self.assertEqual(response.status_code,404)

class PredictionMathTests(TestCase):

    def test_probabilities_sum_to_one(self):

        result = predict_match(1.5, 1.2)

        total = (
            result["home_win"] +
            result["draw"] +
            result["away_win"]
        )

        self.assertAlmostEqual(total, 1.0, places=2)

    def test_scoreline_probabilities_valid(self):

        result = predict_match(1.8,1.1)

        scorelines = result["scoreline_probabilities"]

        for s in scorelines:
            self.assertGreaterEqual(s["probability"], 0)
            self.assertLessEqual(s["probability"],1)