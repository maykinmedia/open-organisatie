from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.contactpersoon import ContactpersoonFactory
from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory
from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.scim.models.factories.team import TeamFactory

from .api_testcase import APITestCase


class ContactpersoonAPITests(APITestCase):
    def test_list_contactpersonen(self):
        ContactpersoonFactory.create_batch(2)
        url = reverse("scim_api:contactpersoon-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contactpersoon_detail(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        org_1 = OrganisatorischeEenheidFactory()
        medewerker_1 = MedewerkerFactory()
        contactpersoon = ContactpersoonFactory(
            teams=[team_1, team_2],
            organisatorische_eenheden=[org_1],
            medewerker=medewerker_1,
        )

        detail_url = reverse(
            "scim_api:contactpersoon-detail", kwargs={"uuid": str(contactpersoon.uuid)}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(contactpersoon.uuid))
        self.assertEqual(
            data["medewerker"]["uuid"], str(contactpersoon.medewerker.uuid)
        )
        self.assertEqual(len(data["teams"]), contactpersoon.teams.count())
        self.assertSetEqual(
            {t["uuid"] for t in data["teams"]},
            set(str(t.uuid) for t in contactpersoon.teams.all()),
        )
        self.assertEqual(
            len(data["organisatorischeEenheden"]),
            contactpersoon.organisatorische_eenheden.count(),
        )
        self.assertSetEqual(
            {o["uuid"] for o in data["organisatorischeEenheden"]},
            set(str(o.uuid) for o in contactpersoon.organisatorische_eenheden.all()),
        )

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:contactpersoon-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medewerker_filter(self):
        medewerker_1 = MedewerkerFactory()
        cp_1 = ContactpersoonFactory(medewerker=medewerker_1)
        ContactpersoonFactory()

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(url, {"medewerkerUuid": str(medewerker_1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_team_filter(self):
        team_1 = TeamFactory()
        cp_1 = ContactpersoonFactory(teams=[team_1])
        ContactpersoonFactory()

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(url, {"teamsUuid": str(team_1.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_organisatorische_eenheid_filter(self):
        organisatorische_eenheid_1 = OrganisatorischeEenheidFactory()
        cp_1 = ContactpersoonFactory(
            organisatorische_eenheden=[organisatorische_eenheid_1]
        )
        ContactpersoonFactory()

        url = reverse("scim_api:contactpersoon-list")
        response = self.client.get(
            url, {"organisatorischeEenhedenUuid": str(organisatorische_eenheid_1.uuid)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_create_contactpersoon(self):
        medewerker = MedewerkerFactory()
        team = TeamFactory()
        org = OrganisatorischeEenheidFactory()

        url = reverse("scim_api:contactpersoon-list")
        payload = {
            "medewerker_uuid": str(medewerker.uuid),
            "teams_uuid": [str(team.uuid)],
            "organisatorische_eenheden_uuid": [str(org.uuid)],
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["medewerker"]["uuid"], str(medewerker.uuid))
        self.assertEqual(len(data["teams"]), 1)
        self.assertEqual(data["teams"][0]["uuid"], str(team.uuid))
        self.assertEqual(len(data["organisatorischeEenheden"]), 1)
        self.assertEqual(data["organisatorischeEenheden"][0]["uuid"], str(org.uuid))

    def test_update_contactpersoon(self):
        cp = ContactpersoonFactory()
        new_team = TeamFactory()
        new_org = OrganisatorischeEenheidFactory()
        url = reverse("scim_api:contactpersoon-detail", kwargs={"uuid": str(cp.uuid)})

        payload = {
            "medewerker_uuid": str(cp.medewerker.uuid),
            "teams_uuid": [str(new_team.uuid)],
            "organisatorische_eenheden_uuid": [str(new_org.uuid)],
        }

        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["teams"]), 1)
        self.assertEqual(data["teams"][0]["uuid"], str(new_team.uuid))
        self.assertEqual(len(data["organisatorischeEenheden"]), 1)
        self.assertEqual(data["organisatorischeEenheden"][0]["uuid"], str(new_org.uuid))

    def test_partial_update_contactpersoon(self):
        cp = ContactpersoonFactory()
        new_org = OrganisatorischeEenheidFactory()
        url = reverse("scim_api:contactpersoon-detail", kwargs={"uuid": str(cp.uuid)})

        payload = {
            "organisatorische_eenheden_uuid": [str(new_org.uuid)],
        }

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["organisatorischeEenheden"]), 1)
        self.assertEqual(data["organisatorischeEenheden"][0]["uuid"], str(new_org.uuid))

    def test_delete_contactpersoon(self):
        cp = ContactpersoonFactory()
        url = reverse("scim_api:contactpersoon-detail", kwargs={"uuid": str(cp.uuid)})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
