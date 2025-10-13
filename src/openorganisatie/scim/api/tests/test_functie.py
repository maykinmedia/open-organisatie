from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.functie import (
    FunctieFactory,
    FunctieTypeFactory,
)

from .api_testcase import APITestCase


class FunctieAPITests(APITestCase):
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
