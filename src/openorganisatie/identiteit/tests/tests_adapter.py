import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from psycopg.types.range import DateRange
from rest_framework.authtoken.models import Token
from reversion.models import Version

from openorganisatie.identiteit.models.relaties import UserGroup

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
        adapter = self.adapter
        adapter.save()
        m = User.objects.get(pk=self.medewerker.pk)
        self.assertEqual(str(m.username), "Test@test.nl")
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
            email="Kees@test.com",
            is_active=True,
        )
        self.user2 = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username=str(uuid.uuid4()),
            email="bob@test.com",
            is_active=True,
        )
        self.team = Group.objects.create(
            name="Test Team", scim_external_id=uuid.uuid4()
        )
        UserGroup.objects.create(
            user=self.user1,
            group=self.team,
            periode=DateRange(timezone.now().date() - timedelta(days=5), None),
        )

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

        membership = UserGroup.objects.get(
            user=self.user1,
            group=self.team,
        )

        self.assertIsNotNone(membership.periode.upper)

    def test_handle_remove_invalid_members(self):
        member_data = [{"value": str(uuid.uuid4())}]
        path = Path(("members", None, None))

        self.adapter.handle_remove(path, member_data, operation=None)
        self.assertIn(self.user1, self.team.user_set.all())

    def test_overlapping_membership_same_user_same_group_fails(self):
        today = timezone.now().date()

        overlapping = UserGroup(
            user=self.user1,
            group=self.team,
            periode=DateRange(
                today - timedelta(days=1),
                today + timedelta(days=5),
            ),
        )

        with self.assertRaises(Exception):
            overlapping.full_clean()

    def test_non_overlapping_membership_same_user_same_group_succeeds(self):
        today = timezone.now().date()

        membership = UserGroup(
            user=self.user1,
            group=self.team,
            periode=DateRange(
                today + timedelta(days=5),
                today + timedelta(days=10),
            ),
        )

        membership.full_clean()
        membership.save()

        self.assertEqual(
            UserGroup.objects.filter(
                user=self.user1,
                group=self.team,
            ).count(),
            2,
        )

    def test_overlapping_membership_different_group_succeeds(self):
        today = timezone.now().date()

        other_group = Group.objects.create(
            name="Other Team",
            scim_external_id=uuid.uuid4(),
        )

        membership = UserGroup(
            user=self.user1,
            group=other_group,
            periode=DateRange(
                today - timedelta(days=1),
                today + timedelta(days=5),
            ),
        )

        membership.full_clean()
        membership.save()

        self.assertEqual(
            UserGroup.objects.filter(user=self.user1).count(),
            2,
        )

    def test_overlapping_membership_different_user_succeeds(self):
        today = timezone.now().date()

        membership = UserGroup(
            user=self.user2,
            group=self.team,
            periode=DateRange(
                today - timedelta(days=1),
                today + timedelta(days=5),
            ),
        )

        membership.full_clean()
        membership.save()

        self.assertEqual(
            UserGroup.objects.filter(group=self.team).count(),
            2,
        )
