from datetime import date, datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory
from openorganisatie.scim.models.factories.team import TeamFactory

from .api_testcase import APITestCase


class MedewerkerAPITests(APITestCase):
    def test_list_medewerkers(self):
        url = reverse("scim_api:medewerker-list")
        MedewerkerFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_medewerker_detail(self):
        medewerker = MedewerkerFactory()

        detail_url = reverse(
            "scim_api:medewerker-detail", kwargs={"oid": str(medewerker.username)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["oid"], str(medewerker.username))
        self.assertEqual(data["voornaam"], medewerker.first_name)
        self.assertEqual(data["achternaam"], medewerker.last_name)
        self.assertEqual(data["emailadres"], medewerker.email)

    def test_authentication_required(self):
        client = APIClient()

        url = reverse("scim_api:medewerker-list")
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_functie(self):
        m1 = MedewerkerFactory(job_title="Developer")
        MedewerkerFactory(job_title="Manager")

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"functie": "developer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["functie"], m1.job_title)

    def test_filter_geslachtsaanduiding(self):
        m1 = MedewerkerFactory(gender_indicator=True)
        MedewerkerFactory(gender_indicator=False)

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"geslachtsaanduiding": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["geslachtsaanduiding"], m1.gender_indicator
        )

    def test_filter_datum_uit_dienst(self):
        m1 = MedewerkerFactory(termination_date=date(2025, 1, 1))
        MedewerkerFactory(termination_date=date(2026, 1, 1))

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"datum_uit_dienst": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["datum_uit_dienst"],
            m1.termination_date.isoformat(),
        )

    def test_filter_actief(self):
        m1 = MedewerkerFactory(is_active=True)
        MedewerkerFactory(is_active=False)

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"actief": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["actief"], m1.is_active)

    def test_filter_teams(self):
        team1 = TeamFactory(scim_external_id="T1")
        team2 = TeamFactory(scim_external_id="T2")

        m1 = MedewerkerFactory()
        m1.scim_groups.add(team1)

        MedewerkerFactory().scim_groups.add(team2)

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"teams": [team1.scim_external_id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_datum_toegevoegd(self):
        m1 = MedewerkerFactory(date_joined=make_aware(datetime(2025, 1, 1)))
        MedewerkerFactory(date_joined=make_aware(datetime(2026, 1, 1)))

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"datum_toegevoegd": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["datum_toegevoegd"], m1.date_joined.isoformat()
        )
