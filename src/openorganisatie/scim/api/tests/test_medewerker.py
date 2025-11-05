from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.scim.enums.enums import GenderIndicator
from openorganisatie.scim.models.factories.functie import FunctieFactory
from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory
from openorganisatie.scim.models.factories.team import TeamFactory

from ...models import Medewerker
from .api_testcase import APITestCase


class MedewerkerAPITests(APITestCase):
    def test_create_medewerker(self):
        url = reverse("scim_api:medewerker-list")
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
        url = reverse("scim_api:medewerker-list")
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
            "scim_api:medewerker-detail", kwargs={"uuid": str(medewerker.uuid)}
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
            "scim_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
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
            "scim_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        patch_data = {"voornaam": "Klaas"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        medewerker.refresh_from_db()
        self.assertEqual(medewerker.voornaam, patch_data["voornaam"])

    def test_delete_medewerker(self):
        medewerker = MedewerkerFactory()
        detail_url = reverse(
            "scim_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Medewerker.objects.filter(uuid=medewerker.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()

        url = reverse("scim_api:medewerker-list")
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_geslachtsaanduiding(self):
        m1 = MedewerkerFactory(geslachtsaanduiding=GenderIndicator.MAN)
        MedewerkerFactory(geslachtsaanduiding=GenderIndicator.VROUW)

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"geslachtsaanduiding": GenderIndicator.MAN})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["geslachtsaanduiding"], m1.geslachtsaanduiding
        )

    def test_filter_teams_uuid(self):
        team1 = TeamFactory()
        team2 = TeamFactory()
        m1 = MedewerkerFactory()
        m1.teams.add(team1)
        MedewerkerFactory().teams.add(team2)

        url = reverse("scim_api:medewerker-list")
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

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(url, {"functiesUuid": str(functie1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(m1.uuid))

    def test_history(self):
        url = reverse("scim_api:medewerker-list")
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
            "scim_api:medewerker-detail", kwargs={"uuid": medewerker.uuid}
        )

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(medewerker).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"voornaam": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(medewerker).count(), 3)
