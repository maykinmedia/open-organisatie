from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.functie import FunctieFactory
from openorganisatie.scim.models.factories.team import TeamFactory
from openorganisatie.scim.models.factories.vestiging import VestigingFactory

from .api_testcase import APITestCase


class TeamAPITests(APITestCase):
    def test_list_teams(self):
        url = reverse("scim_api:team-list")
        TeamFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for team in data:
            self.assertIn("uuid", team)
            self.assertIn("naam", team)
            self.assertIn("beschrijving", team)

    def test_team_detail(self):
        vest1 = VestigingFactory()
        func = FunctieFactory()

        team = TeamFactory(branches=[vest1], functies=[func])

        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(team.uuid))
        self.assertEqual(data["naam"], team.name)
        self.assertEqual(data["beschrijving"], team.description)

        self.assertIn("vestigingen", data)
        self.assertIn("functies", data)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:team-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_naam(self):
        team1 = TeamFactory(name="Finance Team")
        TeamFactory(name="HR Team")

        url = reverse("scim_api:team-list")
        response = self.client.get(url, {"naam": "finance"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["naam"], team1.name)

    def test_filter_vestigingen_uuid(self):
        vest1 = VestigingFactory()
        vest2 = VestigingFactory()
        team1 = TeamFactory(branches=[vest1])
        TeamFactory(branches=[vest2])

        url = reverse("scim_api:team-list")
        response = self.client.get(url, {"vestigingenUuid": str(vest1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(team1.uuid))

    def test_filter_functies_uuid(self):
        functie1 = FunctieFactory()
        functie2 = FunctieFactory()
        team1 = TeamFactory()
        team2 = TeamFactory()
        team1.functies.add(functie1)
        team2.functies.add(functie2)

        url = reverse("scim_api:team-list")
        response = self.client.get(url, {"functiesUuid": str(functie1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(team1.uuid))
