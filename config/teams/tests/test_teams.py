from django.test import TestCase
from rest_framework.test import APIClient
from teams.models import Team


class TeamEndpointTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.team1 = Team.objects.create(name="Newcastle")


    def test_team_list(self):

        response = self.client.get("/api/teams/")

        self.assertEqual(response.status_code, 200)


    def test_team_search(self):

        response = self.client.get("/api/teams/?search=new")

        self.assertEqual(response.status_code, 200)

    
    def test_match_filter_by_team(self):

        response = self.client.get(
            f"/api/matches/?home_team={self.team1.id}"
        )

        self.assertEqual(response.status_code, 200)