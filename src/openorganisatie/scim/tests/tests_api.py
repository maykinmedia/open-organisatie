import json

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from openorganisatie.scim.models.medewerker import Medewerker


class SCIMUsersApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = "/scim/v2/Users"

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
        return Medewerker.objects.get(azure_oid=self.created_user_azure_oid)

    def test_read_user(self):
        medewerker = self.create_user_for_tests()

        response = self.client.get(
            f"{self.url}/{medewerker.azure_oid}", **self._auth_headers()
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
            f"{self.url}/{medewerker.azure_oid}",
            data=json.dumps(update_payload),
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        medewerker.refresh_from_db()
        self.assertEqual(medewerker.voornaam, "Janet")

    def test_delete_user(self):
        medewerker = self.create_user_for_tests()

        response = self.client.delete(
            f"{self.url}/{medewerker.azure_oid}", **self._auth_headers()
        )
        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Medewerker.objects.filter(azure_oid=self.created_user_azure_oid).exists()
        )
