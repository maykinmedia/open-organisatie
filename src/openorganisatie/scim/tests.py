from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models.medewerker import Medewerker

User = get_user_model()


class SCIMUserAPITests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        token, _ = Token.objects.get_or_create(user=self.test_user)

        self.client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        self.medewerker = Medewerker.objects.create(
            medewerker_id="12345",
            voornaam="Jan",
            achternaam="Jansen",
            emailadres="jan.jansen@example.com",
            functie="Developer",
            telefoonnummer="0123456789",
            geslachtsaanduiding=True,
            actief=True,
        )
        self.list_url = reverse("scim:user-list")

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)

    def test_retrieve_user(self):
        url = reverse("scim:user-detail", args=[self.medewerker.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["userName"], self.medewerker.emailadres)

    def test_create_user(self):
        payload = {
            "medewerker_id": "54321",
            "userName": "new.user@example.com",
            "name": {"givenName": "New", "familyName": "User"},
            "active": True,
            "phoneNumbers": [{"value": "0987654321", "type": "work"}],
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medewerker.objects.count(), 2)
        new_user = Medewerker.objects.get(emailadres="new.user@example.com")
        self.assertEqual(new_user.voornaam, "New")
        self.assertEqual(new_user.telefoonnummer, "0987654321")

    def test_update_user(self):
        url = reverse("scim:user-detail", args=[self.medewerker.pk])
        payload = {
            "userName": "updated.email@example.com",
            "name": {"givenName": "JanUpdated", "familyName": "JansenUpdated"},
            "active": False,
            "phoneNumbers": [{"value": "111222333", "type": "work"}],
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medewerker.refresh_from_db()
        self.assertEqual(self.medewerker.emailadres, "updated.email@example.com")
        self.assertEqual(self.medewerker.voornaam, "JanUpdated")
        self.assertEqual(self.medewerker.actief, False)
        self.assertEqual(self.medewerker.telefoonnummer, "111222333")

    def test_delete_user(self):
        url = reverse("scim:user-detail", args=[self.medewerker.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Medewerker.objects.filter(pk=self.medewerker.pk).exists())
