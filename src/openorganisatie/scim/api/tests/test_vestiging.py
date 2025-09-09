from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.scim.models.factories.vestiging import VestigingFactory

from .api_testcase import APITestCase

User = get_user_model()


class VestigingAPITests(APITestCase):
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

    def test_vestigingsnummer_filter(self):
        v1 = VestigingFactory(branchnumber="123")
        VestigingFactory(branchnumber="456")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"vestigingsnummer": "123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["vestigingsnummer"], v1.branchnumber
        )

    def test_naam_filter(self):
        v1 = VestigingFactory(branchname="Amsterdam")
        VestigingFactory(branchname="Rotterdam")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"naam": "Amsterdam"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["naam"], v1.branchname)

    def test_korte_naam_filter(self):
        v1 = VestigingFactory(short_name="AMS")
        VestigingFactory(short_name="RTM")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"korte_naam": "AMS"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["korte_naam"], v1.short_name)

    def test_adres_filter(self):
        v1 = VestigingFactory(address="Straat 1")
        VestigingFactory(address="Straat 2")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"adres": "Straat 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["adres"], v1.address)

    def test_correspondentieadres_filter(self):
        v1 = VestigingFactory(correspondence_address="Co adres")
        VestigingFactory(correspondence_address="ander adres 2")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"correspondentieadres": "Co adres"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["correspondentieadres"],
            v1.correspondence_address,
        )

    def test_postadres_filter(self):
        v1 = VestigingFactory(postal_address="1000AB")
        VestigingFactory(postal_address="2000CD")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"postadres": "1000AB"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["postadres"], v1.postal_address)

    def test_telefoonnummer_filter(self):
        v1 = VestigingFactory(phone_number="0612345678")
        VestigingFactory(phone_number="06876543921")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"telefoonnummer": "0612345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["telefoonnummer"], v1.phone_number)

    def test_landcode_filter(self):
        v1 = VestigingFactory(country_code="NL")
        VestigingFactory(country_code="BE")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"landcode": "NL"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["landcode"], v1.country_code)
