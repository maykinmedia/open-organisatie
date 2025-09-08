from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.contactpersoon import ContactpersoonFactory

User = get_user_model()


class ContactpersoonAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_list_contactpersonen(self):
        url = reverse("scim_api:contactpersoon-list")
        ContactpersoonFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contactpersoon_detail(self):
        contactpersoon = ContactpersoonFactory()

        detail_url = reverse(
            "scim_api:contactpersoon-detail", kwargs={"uuid": str(contactpersoon.uuid)}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(contactpersoon.uuid))
        self.assertEqual(data["naam"], contactpersoon.name)
        self.assertEqual(data["functie"], contactpersoon.function)
        self.assertEqual(data["emailadres"], contactpersoon.email_address)
        self.assertEqual(data["telefoonnummer"], contactpersoon.phone_number)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:contactpersoon-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_naam_filter(self):
        cp_1 = ContactpersoonFactory(name="Tim")
        ContactpersoonFactory(name="Bob")

        url = reverse("scim_api:contactpersoon-list")

        response = self.client.get(url, {"naam": "Tim"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))

    def test_functie_filter(self):
        cp_1 = ContactpersoonFactory(function="Manager")
        ContactpersoonFactory(function="Developer")

        url = reverse("scim_api:contactpersoon-list")

        response = self.client.get(url, {"functie": "Manager"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertCountEqual(
            [cp["uuid"] for cp in response.data["results"]],
            [str(cp_1.uuid)],
        )

    def test_combined_naam_functie_filter(self):
        cp_1 = ContactpersoonFactory(name="Tim", function="Developer")
        ContactpersoonFactory(name="Bob", function="Manager")

        url = reverse("scim_api:contactpersoon-list")

        response = self.client.get(url, {"naam": "Tim", "functie": "Developer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(cp_1.uuid))
