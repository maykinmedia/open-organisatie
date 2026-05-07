from datetime import date, datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.medewerker import MedewerkerFactory
from openorganisatie.organisatie.models.factories.team import TeamFactory
from openorganisatie.organisatie.models.factories.vestiging import VestigingFactory

from ...models.team import Team
from .api_testcase import APITestCase


class TeamAPITests(APITestCase):
    def test_create_team(self):
        url = reverse("organisatie_api:team-list")
        data = {"naam": "Nieuw Team", "omschrijving": "Omschrijving van het team"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        team = Team.objects.get(uuid=response.data["uuid"])
        self.assertEqual(team.naam, data["naam"])
        self.assertEqual(team.omschrijving, data["omschrijving"])

    def test_list_teams(self):
        url = reverse("organisatie_api:team-list")
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

        detail_url = reverse("organisatie_api:team-detail", kwargs={"uuid": team.uuid})
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
        detail_url = reverse("organisatie_api:team-detail", kwargs={"uuid": team.uuid})

        data = {"naam": "Bijgewerkt Team", "omschrijving": "Bijgewerkte omschrijving"}
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team.refresh_from_db()
        self.assertEqual(team.naam, data["naam"])
        self.assertEqual(team.omschrijving, data["omschrijving"])

    def test_partial_update_team(self):
        team = TeamFactory()
        detail_url = reverse("organisatie_api:team-detail", kwargs={"uuid": team.uuid})

        patch_data = {"naam": "Gedeeltelijk Bijgewerkt"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team.refresh_from_db()
        self.assertEqual(team.naam, patch_data["naam"])

    def test_delete_team(self):
        team = TeamFactory()
        detail_url = reverse("organisatie_api:team-detail", kwargs={"uuid": team.uuid})

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(uuid=team.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("organisatie_api:team-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_naam(self):
        team1 = TeamFactory(naam="Finance Team")
        TeamFactory(naam="HR Team")

        url = reverse("organisatie_api:team-list")
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

        url = reverse("organisatie_api:team-list")
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

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"functiesUuid": str(functie1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(team1.uuid))

    def test_filter_external_id(self):
        team1 = TeamFactory()
        TeamFactory()

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"external_id": str(team1.external_id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["externalId"], str(team1.external_id))

    def test_create_team_with_contactpersoon(self):
        url = reverse("organisatie_api:team-list")

        medewerker = MedewerkerFactory()

        data = {
            "naam": "Nieuw Team",
            "omschrijving": "Testteam",
            "contactpersoon_uuid": str(medewerker.uuid),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("contactpersoon", response.data)
        self.assertEqual(response.data["contactpersoon"]["uuid"], str(medewerker.uuid))

    def test_history(self):
        url = reverse("organisatie_api:team-list")
        data = {"naam": "test"}

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            team = Team.objects.get()
            self.assertEqual(Version.objects.get_for_object(team).count(), 1)

        detail_url = reverse("organisatie_api:team-detail", kwargs={"uuid": team.uuid})

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(team).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"naam": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(team).count(), 3)

    def test_filter_startdatum(self):
        t1 = TeamFactory(startdatum=date(2025, 1, 1))
        TeamFactory(startdatum=date(2026, 1, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"startdatum": "2025-01-01"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], t1.startdatum.isoformat()
        )

    def test_filter_startdatum_gte(self):
        TeamFactory(startdatum=date(2024, 12, 31))
        t2 = TeamFactory(startdatum=date(2025, 2, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"startdatum__gte": "2025-01-01"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], t2.startdatum.isoformat()
        )

    def test_filter_startdatum_lte(self):
        t1 = TeamFactory(startdatum=date(2024, 12, 31))
        TeamFactory(startdatum=date(2025, 3, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"startdatum__lte": "2025-01-31"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], t1.startdatum.isoformat()
        )

    def test_filter_einddatum(self):
        t1 = TeamFactory(einddatum=date(2025, 1, 1))
        TeamFactory(einddatum=date(2026, 1, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"einddatum": "2025-01-01"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], t1.einddatum.isoformat()
        )

    def test_filter_einddatum_gte(self):
        TeamFactory(einddatum=date(2024, 12, 31))
        t2 = TeamFactory(einddatum=date(2025, 2, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"einddatum__gte": "2025-01-01"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], t2.einddatum.isoformat()
        )

    def test_filter_einddatum_lte(self):
        t1 = TeamFactory(einddatum=date(2024, 12, 31))
        TeamFactory(einddatum=date(2025, 3, 1))

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"einddatum__lte": "2025-01-31"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], t1.einddatum.isoformat()
        )

    def test_filter_wijzigingsdatum(self):
        dt1 = make_aware(datetime(2025, 1, 1, 10, 30))
        dt2 = make_aware(datetime(2026, 1, 1, 12, 0))
        t1 = TeamFactory(wijzigingsdatum=dt1)
        TeamFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:team-list")
        response = self.client.get(url, {"wijzigingsdatum": dt1.isoformat()})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            t1.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_gte(self):
        make_aware(datetime(2024, 12, 31, 9, 0))
        dt2 = make_aware(datetime(2025, 2, 1, 15, 45))
        t2 = TeamFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:team-list")
        response = self.client.get(
            url, {"wijzigingsdatum__gte": "2025-01-01T00:00:00Z"}
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            t2.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_lte(self):
        dt1 = make_aware(datetime(2024, 12, 31, 8, 0))
        dt2 = make_aware(datetime(2025, 3, 1, 12, 0))
        t1 = TeamFactory(wijzigingsdatum=dt1)
        TeamFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:team-list")
        response = self.client.get(
            url, {"wijzigingsdatum__lte": "2025-01-31T23:59:59Z"}
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            t1.wijzigingsdatum.isoformat(),
        )
