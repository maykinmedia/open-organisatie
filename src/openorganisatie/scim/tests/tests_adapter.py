from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from rest_framework.authtoken.models import Token

from ..adapters import MedewerkerAdapter
from ..models.medewerker import Medewerker


class MedewerkerAdapterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = "/scim/v2/Users"

        self.medewerker = Medewerker.objects.create(
            azure_oid="178fa166-a2cd-4899-8958-8d5eb2eff213",
            voornaam="John",
            achternaam="Doe",
            emailadres="john.doe@example.com",
            actief=True,
        )
        factory = RequestFactory()
        request = factory.get(f"{self.url}/{self.medewerker.azure_oid}")

        self.adapter = MedewerkerAdapter(self.medewerker, request=request)

    def test_to_dict(self):
        result = self.adapter.to_dict()
        self.assertEqual(result["id"], "178fa166-a2cd-4899-8958-8d5eb2eff213")
        self.assertEqual(result["emails"][0]["value"], "john.doe@example.com")
        self.assertTrue(result["active"])
        self.assertIn("schemas", result)
        self.assertEqual(
            result["schemas"], ["urn:ietf:params:scim:schemas:core:2.0:User"]
        )

    def test_from_dict_full(self):
        new_data = {
            "userName": "c5fb5fb9-e72e-40ff-8a26-6fdc8261b043",
            "name": {"givenName": "Jane", "familyName": "Smith"},
            "emails": [{"value": "jane@example.com"}],
            "phoneNumbers": [{"value": "+123456789"}],
            "active": False,
            "jobTitle": "Manager",
        }
        self.adapter.from_dict(new_data)
        m = Medewerker.objects.get(pk=self.medewerker.pk)
        self.assertEqual(str(m.azure_oid), "c5fb5fb9-e72e-40ff-8a26-6fdc8261b043")
        self.assertEqual(m.voornaam, "Jane")
        self.assertEqual(m.achternaam, "Smith")
        self.assertEqual(m.emailadres, "jane@example.com")
        self.assertEqual(m.telefoonnummer, "+123456789")
        self.assertFalse(m.actief)
        self.assertEqual(m.functie, "Manager")

    def test_handle_operations_replace_active(self):
        ops = [{"op": "replace", "path": "active", "value": False}]
        self.adapter.handle_operations(ops)
        m = Medewerker.objects.get(azure_oid=self.medewerker.azure_oid)
        self.assertFalse(m.actief)
