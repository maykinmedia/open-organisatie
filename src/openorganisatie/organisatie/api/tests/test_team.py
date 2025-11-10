from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.team import TeamFactory
from openorganisatie.organisatie.models.factories.vestiging import VestigingFactory

from ...models.team import Team
from .api_testcase import APITestCase


class TeamAPITests(APITestCase):
    def test_create_team(self):
        url = reverse("scim_api:team-list")
        data = {"naam": "Nieuw Team", "omschrijving": "Omschrijving van het team"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        team = Team.objects.get(uuid=response.data["uuid"])
        self.assertEqual(team.naam, data["naam"])
        self.assertEqual(team.omschrijving, data["omschrijving"])

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
            self.assertIn("omschrijving", team)

    def test_team_detail(self):
        vest1 = VestigingFactory()
        func = FunctieFactory()

        team = TeamFactory(vestigingen=[vest1], functies=[func])

        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(team.uuid))
        self.assertEqual(data["naam"], team.naam)
        self.assertEqual(data["omschrijving"], team.omschrijving)

        self.assertIn("vestigingen", data)
        self.assertIn("functies", data)

    def test_update_team(self):
        team = TeamFactory()
        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})

        data = {"naam": "Bijgewerkt Team", "omschrijving": "Bijgewerkte omschrijving"}
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team.refresh_from_db()
        self.assertEqual(team.naam, data["naam"])
        self.assertEqual(team.omschrijving, data["omschrijving"])

    def test_partial_update_team(self):
        team = TeamFactory()
        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})

        patch_data = {"naam": "Gedeeltelijk Bijgewerkt"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team.refresh_from_db()
        self.assertEqual(team.naam, patch_data["naam"])

    def test_delete_team(self):
        team = TeamFactory()
        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(uuid=team.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:team-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_naam(self):
        team1 = TeamFactory(naam="Finance Team")
        TeamFactory(naam="HR Team")

        url = reverse("scim_api:team-list")
        response = self.client.get(url, {"naam": "Finance Team"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["naam"], team1.naam)

    def test_filter_vestigingen_uuid(self):
        vest1 = VestigingFactory()
        vest2 = VestigingFactory()
        team1 = TeamFactory(vestigingen=[vest1])
        TeamFactory(vestigingen=[vest2])

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

    def test_history(self):
        url = reverse("scim_api:team-list")
        data = {"naam": "test"}

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            team = Team.objects.get()
            self.assertEqual(Version.objects.get_for_object(team).count(), 1)

        detail_url = reverse("scim_api:team-detail", kwargs={"uuid": team.uuid})

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(team).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"naam": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(team).count(), 3)
