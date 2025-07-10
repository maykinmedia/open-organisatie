from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.medewerker import MedewerkerFactory

User = get_user_model()


class MedewerkerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_list_medewerkers(self):
        url = reverse("scim_api:medewerker-list")
        MedewerkerFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_medewerker_detail(self):
        medewerker = MedewerkerFactory()

        detail_url = reverse(
            "scim_api:medewerker-detail", kwargs={"username": str(medewerker.username)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["id"], medewerker.pk)
        self.assertEqual(data["username"], str(medewerker.username))
        self.assertEqual(data["first_name"], medewerker.first_name)
        self.assertEqual(data["last_name"], medewerker.last_name)
        self.assertEqual(data["email"], medewerker.email)
