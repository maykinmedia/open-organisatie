from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.functie import FunctieFactory
from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.scim.models.factories.vestiging import VestigingFactory

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
            self.assertIn("soortOrganisatie", org)

    def test_read_organisatorische_eenheid_detail(self):
        vest = VestigingFactory()
        func = FunctieFactory()
        org = OrganisatorischeEenheidFactory(vestigingen=[vest], functies=[func])

        detail_url = reverse(
            "scim_api:organisatorischeeenheid-detail",
            kwargs={"uuid": org.uuid},
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(org.uuid))
        self.assertEqual(data["identificatie"], org.identificatie)
        self.assertEqual(data["naam"], org.naam)
        self.assertEqual(data["soortOrganisatie"], org.soort_organisatie)

        self.assertIn("functies", data)
        self.assertIn("vestigingen", data)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:organisatorischeeenheid-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_identificatie_filter(self):
        org1 = OrganisatorischeEenheidFactory(identificatie="12345")
        OrganisatorischeEenheidFactory(identificatie="6789")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"identificatie": "12345"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["identificatie"], org1.identificatie)

    def test_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(naam="ORG1")
        OrganisatorischeEenheidFactory(naam="ORG2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"naam": "ORG1"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["naam"], org1.naam)

    def test_type_organisatie_filter(self):
        org1 = OrganisatorischeEenheidFactory(soort_organisatie="Type1")
        OrganisatorischeEenheidFactory(soort_organisatie="Type2")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"soortOrganisatie": "Type1"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["soortOrganisatie"], org1.soort_organisatie)

    def test_verkorte_naam_filter(self):
        org1 = OrganisatorischeEenheidFactory(verkorte_naam="FIN")
        OrganisatorischeEenheidFactory(verkorte_naam="HR")

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"verkorteNaam": "FIN"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["verkorteNaam"], org1.verkorte_naam)

    def test_filter_vestiging_uuids(self):
        vest1 = VestigingFactory()
        vest2 = VestigingFactory()
        org1 = OrganisatorischeEenheidFactory()
        org1.vestigingen.add(vest1)

        OrganisatorischeEenheidFactory().vestigingen.add(vest2)

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"vestigingen_uuid": str(vest1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(org1.uuid))

    def test_filter_functie_uuids(self):
        functie1 = FunctieFactory()
        functie2 = FunctieFactory()
        org1 = OrganisatorischeEenheidFactory()
        org1.functies.add(functie1)

        OrganisatorischeEenheidFactory().functies.add(functie2)

        url = reverse("scim_api:organisatorischeeenheid-list")
        response = self.client.get(url, {"functies_uuid": str(functie1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(org1.uuid))

    def test_list_children_under_parent(self):
        parent = OrganisatorischeEenheidFactory()
        child1 = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=parent)
        child2 = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=parent)
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
        child = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=parent)

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

        child1a = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=root1)
        child1b = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=root1)
        child2a = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=root2)

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
        child = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=parent)

        parent.hoofd_organisatorische_eenheid = child
        with self.assertRaises(ValidationError) as val:
            parent.clean()
        self.assertIn(
            "hoofd_organisatorische_eenheid",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan geen kind als bovenliggende eenheid hebben.",
            val.exception.message_dict["hoofd_organisatorische_eenheid"][0],
        )

    def test_prevent_self_parenting(self):
        org = OrganisatorischeEenheidFactory()
        org.hoofd_organisatorische_eenheid = org
        with self.assertRaises(ValidationError) as val:
            org.clean()
        self.assertIn(
            "hoofd_organisatorische_eenheid",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["hoofd_organisatorische_eenheid"][0],
        )
