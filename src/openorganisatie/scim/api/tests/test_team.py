from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.team import TeamFactory

from .api_testcase import APITestCase

User = get_user_model()


class TeamAPITests(APITestCase):
    def test_list_teams(self):
        url = reverse("scim_api:team-list")
        TeamFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for team in data:
            self.assertIn("oid", team)
            self.assertIn("naam", team)
            self.assertIn("beschrijving", team)

    def test_team_detail(self):
        team = TeamFactory()

        detail_url = reverse(
            "scim_api:team-detail", kwargs={"oid": team.scim_external_id}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["oid"], str(team.scim_external_id))
        self.assertEqual(data["naam"], team.name)
        self.assertEqual(data["beschrijving"], team.description)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:team-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
