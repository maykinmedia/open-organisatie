import uuid

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from ..adapters import GroepenAdapter, MedewerkerAdapter
from ..models.medewerker import Medewerker
from ..models.team import Team


class MedewerkerAdapterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)

        self.medewerker = Medewerker.objects.create(
            username="178fa166-a2cd-4899-8958-8d5eb2eff213",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_active=True,
        )

        self.detail_url = reverse(
            "scim:user-detail", kwargs={"uuid": self.medewerker.username}
        )

        factory = RequestFactory()
        request = factory.get(self.detail_url)

        self.adapter = MedewerkerAdapter(self.medewerker, request=request)

    def test_to_dict(self):
        result = self.adapter.to_dict()
        self.assertEqual(result["userName"], "178fa166-a2cd-4899-8958-8d5eb2eff213")
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
        self.assertEqual(str(m.username), "c5fb5fb9-e72e-40ff-8a26-6fdc8261b043")
        self.assertEqual(m.first_name, "Jane")
        self.assertEqual(m.last_name, "Smith")
        self.assertEqual(m.email, "jane@example.com")
        self.assertEqual(m.phone_number, "+123456789")
        self.assertFalse(m.is_active)
        self.assertEqual(m.job_title, "Manager")

    def test_handle_operations_replace_active(self):
        ops = [{"op": "replace", "path": "active", "value": False}]
        self.adapter.handle_operations(ops)
        m = Medewerker.objects.get(username=self.medewerker.username)
        self.assertFalse(m.is_active)


class Path:
    def __init__(self, first_path):
        self.first_path = first_path


class GroepenAdapterTest(TestCase):
    def setUp(self):
        self.user1 = Medewerker.objects.create(
            username=str(uuid.uuid4()),
            first_name="Kees",
            last_name="Smit",
            email="Kees@test.com",
            is_active=True,
        )
        self.user2 = Medewerker.objects.create(
            username=str(uuid.uuid4()),
            first_name="Bob",
            last_name="Smit",
            email="bob@test.com",
            is_active=True,
        )
        self.team = Team.objects.create(name="Test Team", scim_external_id=uuid.uuid4())
        self.team.user_set.add(self.user1)

        factory = RequestFactory()
        self.request = factory.get(
            reverse("scim:group-detail", kwargs={"uuid": self.team.scim_external_id})
        )

        self.adapter = GroepenAdapter(self.team)
        self.adapter.request = self.request

    def test_handle_add_valid_members(self):
        member_data = [{"value": str(self.user2.username)}]
        path = Path(("members", None, None))

        self.adapter.handle_add(path, member_data, operation=None)
        self.assertIn(self.user2, self.team.user_set.all())

    def test_handle_add_invalid_members(self):
        member_data = [{"value": str(uuid.uuid4())}]
        path = Path(("members", None, None))

        self.adapter.handle_add(path, member_data, operation=None)
        self.assertEqual(self.team.user_set.count(), 1)

    def test_handle_remove_valid_members(self):
        member_data = [{"value": str(self.user1.username)}]
        path = Path(("members", None, None))

        self.adapter.handle_remove(path, member_data, operation=None)
        self.assertNotIn(self.user1, self.team.user_set.all())

    def test_handle_remove_invalid_members(self):
        member_data = [{"value": str(uuid.uuid4())}]
        path = Path(("members", None, None))

        self.adapter.handle_remove(path, member_data, operation=None)
        self.assertIn(self.user1, self.team.user_set.all())
