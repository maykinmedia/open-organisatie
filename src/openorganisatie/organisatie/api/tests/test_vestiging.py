from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.vestiging import VestigingFactory

from ...models import Vestiging
from .api_testcase import APITestCase


class VestigingAPITests(APITestCase):
    def test_create_vestiging(self):
        url = reverse("scim_api:vestiging-list")
        data = {
            "vestigingsnummer": "9999",
            "naam": "Nieuwe Vestiging",
            "landcode": "NL",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vestiging = Vestiging.objects.get(uuid=response.data["uuid"])
        self.assertEqual(vestiging.vestigingsnummer, data["vestigingsnummer"])
        self.assertEqual(vestiging.naam, data["naam"])
        self.assertEqual(vestiging.landcode, data["landcode"])

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
        self.assertEqual(data["vestigingsnummer"], vestiging.vestigingsnummer)
        self.assertEqual(data["naam"], vestiging.naam)
        self.assertEqual(data["landcode"], vestiging.landcode)

    def test_update_vestiging(self):
        vestiging = VestigingFactory()
        detail_url = reverse(
            "scim_api:vestiging-detail", kwargs={"uuid": vestiging.uuid}
        )

        data = {
            "vestigingsnummer": vestiging.vestigingsnummer,
            "naam": "Bijgewerkte Vestiging",
            "landcode": "BE",
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vestiging.refresh_from_db()
        self.assertEqual(vestiging.naam, data["naam"])
        self.assertEqual(vestiging.landcode, data["landcode"])

    def test_partial_update_vestiging(self):
        vestiging = VestigingFactory()
        detail_url = reverse(
            "scim_api:vestiging-detail", kwargs={"uuid": vestiging.uuid}
        )

        patch_data = {"naam": "Gedeeltelijk Bijgewerkt"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vestiging.refresh_from_db()
        self.assertEqual(vestiging.naam, patch_data["naam"])

    def test_delete_vestiging(self):
        vestiging = VestigingFactory()
        detail_url = reverse(
            "scim_api:vestiging-detail", kwargs={"uuid": vestiging.uuid}
        )

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vestiging.objects.filter(uuid=vestiging.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:vestiging-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vestigingsnummer_filter(self):
        v1 = VestigingFactory(vestigingsnummer="123")
        VestigingFactory(vestigingsnummer="456")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"vestigingsnummer": "123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["vestigingsnummer"], v1.vestigingsnummer
        )

    def test_naam_filter(self):
        v1 = VestigingFactory(naam="Amsterdam")
        VestigingFactory(naam="Rotterdam")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"naam": "Amsterdam"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["naam"], v1.naam)

    def test_korte_naam_filter(self):
        v1 = VestigingFactory(verkorte_naam="AMS")
        VestigingFactory(verkorte_naam="RTM")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"verkorteNaam": "AMS"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["verkorteNaam"], v1.verkorte_naam)

    def test_adres_filter(self):
        v1 = VestigingFactory(adres="Straat 1")
        VestigingFactory(adres="Straat 2")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"adres": "Straat 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["adres"], v1.adres)

    def test_postadres_filter(self):
        v1 = VestigingFactory(post_adres="1000AB")
        VestigingFactory(post_adres="2000CD")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"postAdres": "1000AB"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["postAdres"], v1.post_adres)

    def test_landcode_filter(self):
        v1 = VestigingFactory(landcode="NL")
        VestigingFactory(landcode="BE")

        url = reverse("scim_api:vestiging-list")
        response = self.client.get(url, {"landcode": "NL"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["landcode"], v1.landcode)

    def test_history(self):
        url = reverse("scim_api:vestiging-list")
        data = {"vestigingsnummer": "1234", "naam": "test"}

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            vestiging = Vestiging.objects.get()
            self.assertEqual(Version.objects.get_for_object(vestiging).count(), 1)

        detail_url = reverse(
            "scim_api:vestiging-detail", kwargs={"uuid": vestiging.uuid}
        )

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(vestiging).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"naam": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(vestiging).count(), 3)
