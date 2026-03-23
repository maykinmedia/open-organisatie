from datetime import date, datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.medewerker import MedewerkerFactory
from openorganisatie.organisatie.models.factories.team import TeamFactory

from ...models import Medewerker
from .api_testcase import APITestCase


class MedewerkerAPITests(APITestCase):
    def test_create_medewerker(self):
        url = reverse("organisatie_api:medewerker-list")
        data = {
            "medewerkerId": "test123",
            "voornaam": "Jan",
            "achternaam": "Jansen",
            "emailadres": "jan.jansen@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        medewerker = Medewerker.objects.get(uuid=response.data["uuid"])
        self.assertEqual(medewerker.medewerker_id, data["medewerkerId"])
        self.assertEqual(medewerker.voornaam, data["voornaam"])
        self.assertEqual(medewerker.achternaam, data["achternaam"])
        self.assertEqual(medewerker.emailadres, data["emailadres"])

    def test_list_medewerkers(self):
        url = reverse("organisatie_api:medewerker-list")
        MedewerkerFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_medewerker_detail(self):
        team = TeamFactory()
        functie = FunctieFactory()
        medewerker = MedewerkerFactory(teams=[team], functies=[functie])

        detail_url = reverse(
            "organisatie_api:medewerker-detail", kwargs={"uuid": str(medewerker.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["medewerkerId"], str(medewerker.medewerker_id))
        self.assertEqual(data["voornaam"], medewerker.voornaam)
        self.assertEqual(data["achternaam"], medewerker.achternaam)
        self.assertEqual(data["emailadres"], medewerker.emailadres)

        self.assertIn("teams", data)
        self.assertIn("functies", data)

    def test_update_medewerker(self):
        medewerker = MedewerkerFactory()
        detail_url = reverse(
            "organisatie_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        data = {
            "medewerkerId": medewerker.medewerker_id,
            "voornaam": "Pieter",
            "achternaam": "Pietersen",
            "emailadres": "pieter.pietersen@example.com",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        medewerker.refresh_from_db()
        self.assertEqual(medewerker.voornaam, data["voornaam"])
        self.assertEqual(medewerker.achternaam, data["achternaam"])
        self.assertEqual(medewerker.emailadres, data["emailadres"])

    def test_partial_update_medewerker(self):
        medewerker = MedewerkerFactory()
        detail_url = reverse(
            "organisatie_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        patch_data = {"voornaam": "Klaas"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        medewerker.refresh_from_db()
        self.assertEqual(medewerker.voornaam, patch_data["voornaam"])

    def test_delete_medewerker(self):
        medewerker = MedewerkerFactory()
        detail_url = reverse(
            "organisatie_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Medewerker.objects.filter(uuid=medewerker.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()

        url = reverse("organisatie_api:medewerker-list")
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_teams_uuid(self):
        team1 = TeamFactory()
        team2 = TeamFactory()
        m1 = MedewerkerFactory()
        m1.teams.add(team1)
        MedewerkerFactory().teams.add(team2)

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"teams_uuid": str(team1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(m1.uuid))

    def test_filter_functies_uuid(self):
        functie1 = FunctieFactory()
        functie2 = FunctieFactory()
        m1 = MedewerkerFactory()
        m1.functies.add(functie1)
        MedewerkerFactory().functies.add(functie2)

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"functiesUuid": str(functie1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(m1.uuid))

    def test_history(self):
        url = reverse("organisatie_api:medewerker-list")
        data = {
            "medewerkerId": "test",
            "voornaam": "test",
            "achternaam": "test",
            "emailadres": "test@gmail.com",
        }

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            medewerker = Medewerker.objects.get()
            self.assertEqual(Version.objects.get_for_object(medewerker).count(), 1)

        detail_url = reverse(
            "organisatie_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(medewerker).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"voornaam": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(medewerker).count(), 3)

    def test_filter_startdatum(self):
        m1 = MedewerkerFactory(startdatum=date(2025, 1, 1))
        MedewerkerFactory(startdatum=date(2026, 1, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"startdatum": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], m1.startdatum.isoformat()
        )

    def test_filter_startdatum_gte(self):
        MedewerkerFactory(startdatum=date(2024, 12, 31))
        m2 = MedewerkerFactory(startdatum=date(2025, 2, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"startdatum__gte": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], m2.startdatum.isoformat()
        )

    def test_filter_startdatum_lte(self):
        m1 = MedewerkerFactory(startdatum=date(2024, 12, 31))
        MedewerkerFactory(startdatum=date(2025, 3, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"startdatum__lte": "2025-01-31"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], m1.startdatum.isoformat()
        )

    def test_filter_einddatum(self):
        m1 = MedewerkerFactory(einddatum=date(2025, 1, 1))
        MedewerkerFactory(einddatum=date(2026, 1, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"einddatum": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], m1.einddatum.isoformat()
        )

    def test_filter_einddatum_gte(self):
        MedewerkerFactory(einddatum=date(2024, 12, 31))
        m2 = MedewerkerFactory(einddatum=date(2025, 2, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"einddatum__gte": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], m2.einddatum.isoformat()
        )

    def test_filter_einddatum_lte(self):
        m1 = MedewerkerFactory(einddatum=date(2024, 12, 31))
        MedewerkerFactory(einddatum=date(2025, 3, 1))

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"einddatum__lte": "2025-01-31"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], m1.einddatum.isoformat()
        )

    def test_filter_wijzigingsdatum(self):
        dt1 = make_aware(datetime(2025, 1, 1, 10, 30))
        dt2 = make_aware(datetime(2026, 1, 1, 12, 0))
        m1 = MedewerkerFactory(wijzigingsdatum=dt1)
        MedewerkerFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(url, {"wijzigingsdatum": dt1.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            m1.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_gte(self):
        make_aware(datetime(2024, 12, 31, 9, 0))
        dt2 = make_aware(datetime(2025, 2, 1, 15, 45))
        m2 = MedewerkerFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(
            url, {"wijzigingsdatum__gte": "2025-01-01T00:00:00Z"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            m2.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_lte(self):
        dt1 = make_aware(datetime(2024, 12, 31, 8, 0))
        dt2 = make_aware(datetime(2025, 3, 1, 12, 0))
        m1 = MedewerkerFactory(wijzigingsdatum=dt1)
        MedewerkerFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:medewerker-list")
        response = self.client.get(
            url, {"wijzigingsdatum__lte": "2025-01-31T23:59:59Z"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            m1.wijzigingsdatum.isoformat(),
        )
