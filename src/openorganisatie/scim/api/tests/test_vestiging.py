from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.vestiging import VestigingFactory

from .api_testcase import APITestCase


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

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:vestiging-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        response = self.client.get(url, {"korteNaam": "AMS"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["korteNaam"], v1.short_name)

    def test_adres_filter(self):
        v1 = VestigingFactory(address="Straat 1")
        VestigingFactory(address="Straat 2")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"adres": "Straat 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["adres"], v1.address)

    def test_postadres_filter(self):
        v1 = VestigingFactory(postal_address="1000AB")
        VestigingFactory(postal_address="2000CD")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"postadres": "1000AB"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["postadres"], v1.postal_address)

    def test_landcode_filter(self):
        v1 = VestigingFactory(country_code="NL")
        VestigingFactory(country_code="BE")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"landcode": "NL"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["landcode"], v1.country_code)
