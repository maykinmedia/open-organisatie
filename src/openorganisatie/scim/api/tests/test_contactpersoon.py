from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.contactpersoon import ContactpersoonFactory
from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory
from openorganisatie.scim.models.factories.team import TeamFactory

from .api_testcase import APITestCase


class ContactpersoonAPITests(APITestCase):
    def test_list_contactpersonen(self):
        ContactpersoonFactory.create_batch(2)  # creates with unique medewerkers
        url = reverse("scim_api:contactpersoon-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contactpersoon_detail(self):
        contactpersoon = ContactpersoonFactory()
        detail_url = reverse(
            "scim_api:contactpersoon-detail", kwargs={"uuid": str(contactpersoon.uuid)}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(contactpersoon.uuid))
        self.assertEqual(data["medewerker"], str(contactpersoon.medewerker))
        self.assertEqual(
            data.get("team"), str(contactpersoon.team) if contactpersoon.team else None
        )
        self.assertEqual(
            data.get("organisatorische_eenheid"),
            str(contactpersoon.organisatorische_eenheid)
            if contactpersoon.organisatorische_eenheid
            else None,
        )

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:contactpersoon-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medewerker_filter(self):
        medewerker_1 = MedewerkerFactory()
        cp_1 = ContactpersoonFactory(medewerker=medewerker_1)
        ContactpersoonFactory()  # unrelated contactpersoon

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(url, {"medewerker": str(medewerker_1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_team_filter(self):
        team_1 = TeamFactory()
        cp_1 = ContactpersoonFactory(team=team_1)
        ContactpersoonFactory()  # another unrelated contactpersoon

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(url, {"team": str(team_1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_combined_medewerker_team_filter(self):
        medewerker_1 = MedewerkerFactory()
        team_1 = TeamFactory()
        cp_1 = ContactpersoonFactory(medewerker=medewerker_1, team=team_1)
        ContactpersoonFactory()  # unrelated contactpersoon

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(
            url, {"medewerker": str(medewerker_1.uuid), "team": str(team_1.uuid)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))
