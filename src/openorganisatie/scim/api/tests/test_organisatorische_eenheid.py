from datetime import date

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)

from .api_testcase import APITestCase


class OrganisatorischeEenheidAPITests(APITestCase):
    def test_list_organisatorische_eenheden(self):
        url = reverse("scim_api:organisatorischeeenheid-list")
        OrganisatorischeEenheidFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

        for org in data["results"]:
            self.assertIn("uuid", org)
            self.assertIn("naam", org)
            self.assertIn("type_organisatie", org)

    def test_read_organisatorische_eenheid_detail(self):
        org = OrganisatorischeEenheidFactory()

        detail_url = reverse(
            "scim_api:organisatorischeeenheid-detail",
            kwargs={"uuid": org.uuid},
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(org.uuid))
        self.assertEqual(data["identificatie"], org.identifier)
        self.assertEqual(data["naam"], org.name)
        self.assertEqual(data["type_organisatie"], org.organization_type)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:organisatorischeeenheid-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_identificatie_filter(self):
        org1 = OrganisatorischeEenheidFactory(identifier="12345")
        OrganisatorischeEenheidFactory(identifier="6789")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"identificatie": "12345"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["identificatie"], org1.identifier)

    def test_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(name="ORG1")
        OrganisatorischeEenheidFactory(name="ORG2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"naam": "Org1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["naam"], org1.name)

    def test_type_organisatie_filter(self):
        org1 = OrganisatorischeEenheidFactory(organization_type="Type1")
        OrganisatorischeEenheidFactory(organization_type="Type2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"type_organisatie": "Type1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["type_organisatie"], org1.organization_type
        )

    def test_verkorte_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(short_name="FIN")
        OrganisatorischeEenheidFactory(short_name="HR")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"verkorte_naam": "FIN"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["verkorte_naam"], org1.short_name)

    def test_beschrijving_filter(self):
        org1 = OrganisatorischeEenheidFactory(description="Finance divisie")
        OrganisatorischeEenheidFactory(description="HR divisie")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"beschrijving": "Finance divisie"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["beschrijving"], org1.description)

    def test_emailadres_filter(self):
        org1 = OrganisatorischeEenheidFactory(email_address="finance@example.com")
        OrganisatorischeEenheidFactory(email_address="hr@example.com")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"emailadres": "finance@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["emailadres"], org1.email_address)

    def test_telefoonnummer_filter(self):
        org1 = OrganisatorischeEenheidFactory(phone_number="0612345678")
        OrganisatorischeEenheidFactory(phone_number="0687654321")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"telefoonnummer": "0612345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["telefoonnummer"], org1.phone_number
        )

    def test_einddatum_filter(self):
        org1 = OrganisatorischeEenheidFactory(end_date=date(2025, 1, 1))
        OrganisatorischeEenheidFactory(end_date=date(2026, 1, 1))

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"einddatum": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], org1.end_date.isoformat()
        )
