from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team
from matches.models import Match



class MatchEndpointTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.team1 = Team.objects.create(name="Spurs")
        self.team2 = Team.objects.create(name="Brighton")

        self.match = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            home_score=2,
            away_score=1,
            season="2324",
            match_date="2023-8-15"
        )

    # Check match list
    def test_match_list(self):

        response = self.client.get("/api/matches/")

        self.assertEqual(response.status_code, 200)

    # Check filtering is enabled
    def test_match_filter_by_team(self):

        response = self.client.get(
            f"/api/matches/?home_team={self.team1.id}"
        )

        self.assertEqual(response.status_code, 200)