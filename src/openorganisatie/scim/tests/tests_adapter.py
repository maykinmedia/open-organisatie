import uuid

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from reversion.models import Version

from ..adapters import GroupAdapter, UserAdapter
from ..models.group import Group
from ..models.user import User


class MedewerkerAdapterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.token = Token.objects.create(user=self.user)

        self.medewerker = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username="Test@test.nl",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_active=True,
        )

        self.detail_url = reverse(
            "scim:user-detail", kwargs={"uuid": self.medewerker.scim_external_id}
        )

        factory = RequestFactory()
        request = factory.get(self.detail_url)

        self.adapter = UserAdapter(self.medewerker, request=request)

    def test_to_dict(self):
        result = self.adapter.to_dict()
        self.assertEqual(result["scimExternalId"], self.medewerker.scim_external_id)
        self.assertEqual(result["userName"], "Test@test.nl")
        self.assertEqual(result["emails"][0]["value"], "john.doe@example.com")
        self.assertTrue(result["active"])
        self.assertIn("schemas", result)
        self.assertEqual(
            result["schemas"], ["urn:ietf:params:scim:schemas:core:2.0:User"]
        )

    def test_from_dict_full(self):
        m = User.objects.get(pk=self.medewerker.pk)
        self.assertEqual(str(m.username), "Test@test.nl")
        self.assertEqual(m.first_name, "John")
        self.assertEqual(m.last_name, "Doe")
        self.assertEqual(m.email, "john.doe@example.com")

        self.assertEqual(Version.objects.get_for_object(m).count(), 1)

    def test_handle_operations_replace_active(self):
        ops = [{"op": "replace", "path": "active", "value": False}]
        self.adapter.handle_operations(ops)
        m = User.objects.get(username=self.medewerker.username)
        self.assertFalse(m.is_active)


class Path:
    def __init__(self, first_path):
        self.first_path = first_path


class GroepenAdapterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username=str(uuid.uuid4()),
            first_name="Kees",
            last_name="Smit",
            email="Kees@test.com",
            is_active=True,
        )
        self.user2 = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username=str(uuid.uuid4()),
            first_name="Bob",
            last_name="Smit",
            email="bob@test.com",
            is_active=True,
        )
        self.team = Group.objects.create(
            name="Test Team", scim_external_id=uuid.uuid4()
        )
        self.team.user_set.add(self.user1)

        factory = RequestFactory()
        self.request = factory.get(
            reverse("scim:group-detail", kwargs={"uuid": self.team.scim_external_id})
        )

        self.adapter = GroupAdapter(self.team)
        self.adapter.request = self.request

    def test_handle_add_valid_members(self):
        member_data = [{"value": str(self.user2.scim_external_id)}]
        path = Path(("members", None, None))

        self.adapter.handle_add(path, member_data, operation=None)
        self.assertIn(self.user2, self.team.user_set.all())

    def test_handle_add_invalid_members(self):
        member_data = [{"value": str(uuid.uuid4())}]
        path = Path(("members", None, None))

        self.adapter.handle_add(path, member_data, operation=None)
        self.assertEqual(self.team.user_set.count(), 1)

    def test_handle_remove_valid_members(self):
        member_data = [{"value": str(self.user1.scim_external_id)}]
        path = Path(("members", None, None))

        self.adapter.handle_remove(path, member_data, operation=None)
        self.assertNotIn(self.user1, self.team.user_set.all())

    def test_handle_remove_invalid_members(self):
        member_data = [{"value": str(uuid.uuid4())}]
        path = Path(("members", None, None))

        self.adapter.handle_remove(path, member_data, operation=None)
        self.assertIn(self.user1, self.team.user_set.all())
