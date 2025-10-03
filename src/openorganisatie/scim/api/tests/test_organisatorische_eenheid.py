from datetime import date

from django.core.exceptions import ValidationError
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
            self.assertIn("typeOrganisatie", org)

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
        self.assertEqual(data["typeOrganisatie"], org.organization_type)

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
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["identificatie"], org1.identifier)

    def test_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(name="ORG1")
        OrganisatorischeEenheidFactory(name="ORG2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"naam": "Org1"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["naam"], org1.name)

    def test_type_organisatie_filter(self):
        org1 = OrganisatorischeEenheidFactory(organization_type="Type1")
        OrganisatorischeEenheidFactory(organization_type="Type2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"typeOrganisatie": "Type1"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["typeOrganisatie"], org1.organization_type)

    def test_verkorte_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(short_name="FIN")
        OrganisatorischeEenheidFactory(short_name="HR")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"verkorteNaam": "FIN"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["verkorteNaam"], org1.short_name)

    def test_beschrijving_filter(self):
        org1 = OrganisatorischeEenheidFactory(description="Finance divisie")
        OrganisatorischeEenheidFactory(description="HR divisie")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"beschrijving": "Finance divisie"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["beschrijving"], org1.description)

    def test_emailadres_filter(self):
        org1 = OrganisatorischeEenheidFactory(email_address="finance@example.com")
        OrganisatorischeEenheidFactory(email_address="hr@example.com")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"emailadres": "finance@example.com"})

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["emailadres"], org1.email_address)

    def test_telefoonnummer_filter(self):
        org1 = OrganisatorischeEenheidFactory(phone_number="0612345678")
        OrganisatorischeEenheidFactory(phone_number="0687654321")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"telefoonnummer": "0612345678"})

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["telefoonnummer"], org1.phone_number)

    def test_einddatum_filter(self):
        org1 = OrganisatorischeEenheidFactory(end_date=date(2025, 1, 1))
        OrganisatorischeEenheidFactory(end_date=date(2026, 1, 1))

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"einddatum": "2025-01-01"})

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["einddatum"], org1.end_date.isoformat())

    def test_list_children_under_parent(self):
        parent = OrganisatorischeEenheidFactory()
        child1 = OrganisatorischeEenheidFactory(parent_organisation=parent)
        child2 = OrganisatorischeEenheidFactory(parent_organisation=parent)
        OrganisatorischeEenheidFactory()

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        children = [
            org
            for org in response.data["results"]
            if org.get("hoofd_organisatorische_eenheid") == str(parent.uuid)
        ]
        self.assertIn(str(child1.uuid), [c["uuid"] for c in children])
        self.assertIn(str(child2.uuid), [c["uuid"] for c in children])

    def test_parent_field_in_detail(self):
        parent = OrganisatorischeEenheidFactory()
        child = OrganisatorischeEenheidFactory(parent_organisation=parent)

        url = reverse(
            "scim_api:organisatorischeeenheid-detail", kwargs={"uuid": child.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["hoofd_organisatorische_eenheid"], str(parent.uuid)
        )

    def test_multiple_independent_trees(self):
        root1 = OrganisatorischeEenheidFactory()
        root2 = OrganisatorischeEenheidFactory()

        child1a = OrganisatorischeEenheidFactory(parent_organisation=root1)
        child1b = OrganisatorischeEenheidFactory(parent_organisation=root1)
        child2a = OrganisatorischeEenheidFactory(parent_organisation=root2)

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.data["results"]

        roots = [
            org for org in data if org.get("hoofd_organisatorische_eenheid") is None
        ]
        self.assertIn(str(root1.uuid), [r["uuid"] for r in roots])
        self.assertIn(str(root2.uuid), [r["uuid"] for r in roots])
        self.assertEqual(len(roots), 2)

        children_root1 = [
            org["uuid"]
            for org in data
            if org.get("hoofd_organisatorische_eenheid") == str(root1.uuid)
        ]
        children_root2 = [
            org["uuid"]
            for org in data
            if org.get("hoofd_organisatorische_eenheid") == str(root2.uuid)
        ]

        self.assertIn(str(child1a.uuid), children_root1)
        self.assertIn(str(child1b.uuid), children_root1)
        self.assertIn(str(child2a.uuid), children_root2)

    def test_prevent_cycle_in_parent(self):
        parent = OrganisatorischeEenheidFactory()
        child = OrganisatorischeEenheidFactory(parent_organisation=parent)

        parent.parent_organisation = child
        with self.assertRaises(ValidationError) as val:
            parent.clean()
        self.assertIn(
            "parent_organisation",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan geen kind als bovenliggende eenheid hebben.",
            val.exception.message_dict["parent_organisation"][0],
        )

    def test_prevent_self_parenting(self):
        org = OrganisatorischeEenheidFactory()
        org.parent_organisation = org
        with self.assertRaises(ValidationError) as val:
            org.clean()
        self.assertIn(
            "parent_organisation",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["parent_organisation"][0],
        )
