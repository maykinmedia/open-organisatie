from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.scim.models.factories.functie import (
    FunctieFactory,
    FunctieTypeFactory,
)

from ...models import Functie
from .api_testcase import APITestCase


class FunctieAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.functie_type = FunctieTypeFactory()

    def test_create_functie(self):
        url = reverse("scim_api:functie-list")
        data = {
            "functieOmschrijving": "Nieuwe Functie",
            "beginDatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        functie = Functie.objects.get(uuid=response.data["uuid"])
        self.assertEqual(functie.functie_omschrijving, data["functieOmschrijving"])
        self.assertEqual(functie.begin_datum.isoformat(), data["beginDatum"])

    def test_list_functies(self):
        url = reverse("scim_api:functie-list")
        FunctieFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 3)
        for functie in data["results"]:
            self.assertIn("uuid", functie)
            self.assertIn("functieOmschrijving", functie)
            self.assertIn("beginDatum", functie)

    def test_read_functie_detail(self):
        type1 = FunctieTypeFactory()
        functie = FunctieFactory(functie_type=type1)
        detail_url = reverse("scim_api:functie-detail", kwargs={"uuid": functie.uuid})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(functie.uuid))
        self.assertEqual(data["functieOmschrijving"], functie.functie_omschrijving)
        self.assertEqual(data["beginDatum"], functie.begin_datum.isoformat())

    def test_update_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse("scim_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": "Bijgewerkte Functie",
            "beginDatum": "2025-12-01",
            "functietypeUuid": str(self.functie_type.uuid),
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(functie.functie_omschrijving, data["functieOmschrijving"])
        self.assertEqual(functie.begin_datum.isoformat(), data["beginDatum"])

    def test_partial_update_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse("scim_api:functie-detail", kwargs={"uuid": functie.uuid})

        patch_data = {"functieOmschrijving": "Gedeeltelijk Bijgewerkt"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(
            functie.functie_omschrijving, patch_data["functieOmschrijving"]
        )

    def test_delete_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse("scim_api:functie-detail", kwargs={"uuid": functie.uuid})

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Functie.objects.filter(uuid=functie.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:functie-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_functie_omschrijving(self):
        functie1 = FunctieFactory(functie_omschrijving="Software Engineer")
        FunctieFactory(functie_omschrijving="Data Scientist")

        url = reverse("scim_api:functie-list")
        response = self.client.get(url, {"functie_omschrijving": "Software Engineer"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_filter_functie_type_uuid(self):
        type1 = FunctieTypeFactory()
        type2 = FunctieTypeFactory()

        functie1 = FunctieFactory(functie_type=type1)
        FunctieFactory(functie_type=type2)

        url = reverse("scim_api:functie-list")
        response = self.client.get(url, {"functie_type_uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_history(self):
        url = reverse("scim_api:functie-list")
        data = {
            "functieOmschrijving": "1234",
            "beginDatum": "2025-10-10",
            "functietypeUuid": str(FunctieTypeFactory.create().uuid),
        }

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            functie = Functie.objects.get()
            self.assertEqual(Version.objects.get_for_object(functie).count(), 1)

        detail_url = reverse("scim_api:functie-detail", kwargs={"uuid": functie.uuid})

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functie).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"functieOmschrijving": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functie).count(), 3)
