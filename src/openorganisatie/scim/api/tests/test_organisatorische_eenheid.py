from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)

User = get_user_model()


class OrganisatorischeEenheidAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

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
