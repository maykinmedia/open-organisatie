from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.enums.enums import GenderIndicator
from openorganisatie.scim.models.factories.functie import FunctieFactory
from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory
from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
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
        team = TeamFactory()
        functie = FunctieFactory()
        org = OrganisatorischeEenheidFactory()
        medewerker = MedewerkerFactory(
            teams=[team], functies=[functie], organisatorische_eenheden=[org]
        )

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
        self.assertIn("organisatorischeEenheden", data)

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

    def test_filter_organisatorische_eenheden_uuid(self):
        org1 = OrganisatorischeEenheidFactory()
        org2 = OrganisatorischeEenheidFactory()
        m1 = MedewerkerFactory()
        m1.organisatorische_eenheden.add(org1)
        MedewerkerFactory().organisatorische_eenheden.add(org2)

        url = reverse("scim_api:medewerker-list")
        response = self.client.get(
            url, {"organisatorische_eenheden_uuid": str(org1.uuid)}
        )
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
