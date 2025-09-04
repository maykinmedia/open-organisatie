from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.scim.models.factories.vestiging import VestigingFactory

User = get_user_model()


class VestigingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_list_vestigingen(self):
        url = reverse("scim_api:vestiging-list")
        VestigingFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_vestiging_detail(self):
        vestiging = VestigingFactory()

        detail_url = reverse(
            "scim_api:vestiging-detail", kwargs={"uuid": vestiging.uuid}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["vestigingsnummer"], vestiging.branchnumber)
        self.assertEqual(data["naam"], vestiging.branchname)
        self.assertEqual(data["landcode"], vestiging.country_code)

        org_data = data["organisatorische_eenheid"]
        self.assertEqual(org_data["uuid"], str(vestiging.organisational_unit.uuid))
        self.assertEqual(org_data["naam"], vestiging.organisational_unit.name)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:vestiging-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vestiging_filter_by_organisatie(self):
        org1 = OrganisatorischeEenheidFactory(identifier="OE001", name="Finance")
        org2 = OrganisatorischeEenheidFactory(identifier="OE002", name="HR")

        vest1 = VestigingFactory(organisational_unit=org1)
        VestigingFactory(organisational_unit=org2)

        url = (
            f"{reverse('scim_api:vestiging-list')}?organisatorische_eenheid={org1.uuid}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["vestigingsnummer"], vest1.branchnumber)
