import json

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from openorganisatie.scim.models.medewerker import Medewerker


class SCIMUsersViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = "/scim/v2/Users"

        self.payload = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "userName": "jane.doe@example.com",
            "externalId": "external-123",
            "name": {"givenName": "Jane", "familyName": "Doe"},
            "emails": [{"value": "jane.doe@example.com", "primary": True}],
            "active": True,
        }

    def _auth_headers(self):
        return {
            "HTTP_AUTHORIZATION": f"Bearer {self.token.key}",
            "content_type": "application/json",
        }

    def test_create_user_with_token_auth(self):
        response = self.client.post(
            self.url, data=json.dumps(self.payload), **self._auth_headers()
        )
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.content)
        self.assertIn("id", response_json)
        self.assertEqual(response_json["userName"], "jane.doe@example.com")
        self.resource_id = response_json["id"]

        medewerker = Medewerker.objects.filter(
            emailadres="jane.doe@example.com"
        ).first()
        self.assertIsNotNone(medewerker)
        self.assertEqual(medewerker.voornaam, "Jane")
        self.assertEqual(medewerker.achternaam, "Doe")

    def test_read_user(self):
        self.test_create_user_with_token_auth()
        medewerker = Medewerker.objects.get(emailadres="jane.doe@example.com")

        response = self.client.get(
            f"{self.url}/{medewerker.uuid}", **self._auth_headers()
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["userName"], "jane.doe@example.com")
        self.assertEqual(response_json["name"]["givenName"], "Jane")

    def test_update_user(self):
        self.test_create_user_with_token_auth()
        medewerker = Medewerker.objects.get(emailadres="jane.doe@example.com")

        update_payload = self.payload.copy()
        update_payload["name"]["givenName"] = "Janet"

        response = self.client.put(
            f"{self.url}/{medewerker.uuid}",
            data=json.dumps(update_payload),
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        medewerker.refresh_from_db()
        self.assertEqual(medewerker.voornaam, "Janet")

    def test_delete_user(self):
        self.test_create_user_with_token_auth()
        medewerker = Medewerker.objects.get(emailadres="jane.doe@example.com")

        response = self.client.delete(
            f"{self.url}/{medewerker.uuid}", **self._auth_headers()
        )
        self.assertEqual(response.status_code, 204)

        # Confirm deletion
        self.assertFalse(
            Medewerker.objects.filter(emailadres="jane.doe@example.com").exists()
        )
