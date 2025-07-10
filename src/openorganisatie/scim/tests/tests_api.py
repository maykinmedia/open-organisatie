import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from openorganisatie.scim.models.medewerker import Medewerker


class SCIMUsersApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse("scim:users")

        self.payload = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "userName": "c5fb5fb9-e72e-40ff-8a26-6fdc8261b043",
            "externalId": "external-123",
            "name": {"givenName": "Jane", "familyName": "Doe"},
            "emails": [{"value": "jane.doe@example.com", "primary": True}],
            "active": True,
        }

        response = self.client.post(
            self.url, data=json.dumps(self.payload), **self._auth_headers()
        )
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.content)
        self.created_user_azure_oid = response_json["userName"]

    def _auth_headers(self):
        return {
            "HTTP_AUTHORIZATION": f"Bearer {self.token.key}",
            "content_type": "application/json",
        }

    def create_user_for_tests(self):
        return Medewerker.objects.get(username=self.created_user_azure_oid)

    def test_read_user(self):
        medewerker = self.create_user_for_tests()

        response = self.client.get(
            reverse("scim:user-detail", kwargs={"uuid": medewerker.username}),
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["userName"], self.created_user_azure_oid)
        self.assertEqual(response_json["name"]["givenName"], "Jane")

    def test_update_user(self):
        medewerker = self.create_user_for_tests()

        update_payload = self.payload.copy()
        update_payload["name"]["givenName"] = "Janet"

        response = self.client.put(
            reverse("scim:user-detail", kwargs={"uuid": medewerker.username}),
            data=json.dumps(update_payload),
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        medewerker.refresh_from_db()
        self.assertEqual(medewerker.first_name, "Janet")

    def test_delete_user(self):
        medewerker = self.create_user_for_tests()

        response = self.client.delete(
            reverse("scim:user-detail", kwargs={"uuid": medewerker.username}),
            **self._auth_headers(),
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Medewerker.objects.filter(username=self.created_user_azure_oid).exists()
        )
