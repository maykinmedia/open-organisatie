import uuid
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from psycopg.types.range import DateRange
from rest_framework import status

from openorganisatie.identiteit.models.relaties import UserGroup

from ...models.group import Group
from ...models.user import User
from .api_testcase import APITestCaseBearer


class SCIMApiIntegrationTest(APITestCaseBearer):
    def setUp(self):
        super().setUp()

        self.scim_user = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username="john@example.com",
            email="john@example.com",
            is_active=True,
        )

        self.group = Group.objects.create(
            name="Engineering",
            scim_external_id=uuid.uuid4(),
        )

    def test_entra_id_create_user(self):
        """
        Simulates:
        POST /scim/v2/Users/
        """

        payload = {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User",
                "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
            ],
            "externalId": str(uuid.uuid4()),
            "userName": "alice@example.com",
            "active": True,
            "name": {
                "givenName": "Alice",
                "familyName": "Smith",
            },
            "emails": [
                {
                    "value": "alice@example.com",
                    "primary": True,
                }
            ],
            "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
                "employeeNumber": "EMP001",
            },
        }

        url = reverse("scim:users")

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created = User.objects.get(username="alice@example.com")

        self.assertEqual(created.employee_number, "EMP001")
        self.assertEqual(created.email, "alice@example.com")
        self.assertTrue(created.is_active)

    def test_entra_id_disable_user(self):
        """
        Simulates:
        PATCH /scim/v2/Users/{id}
        active=false
        """

        UserGroup.objects.create(
            user=self.scim_user,
            group=self.group,
            periode=DateRange(
                timezone.now().date() - timedelta(days=10),
                None,
            ),
        )

        url = reverse(
            "scim:user-detail",
            kwargs={"uuid": self.scim_user.scim_external_id},
        )

        payload = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
            "Operations": [
                {
                    "op": "Replace",
                    "path": "active",
                    "value": False,
                }
            ],
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.scim_user.refresh_from_db()

        self.assertFalse(self.scim_user.is_active)

        membership = UserGroup.objects.get(
            user=self.scim_user,
            group=self.group,
        )
        print(membership.periode)

        self.assertIsNotNone(membership.periode.upper)

    def test_entra_id_add_group_member(self):
        """
        Simulates:
        PATCH /scim/v2/Groups/{id}
        add member
        """

        url = reverse(
            "scim:group-detail",
            kwargs={"uuid": self.group.scim_external_id},
        )

        payload = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
            "Operations": [
                {
                    "op": "Add",
                    "path": "members",
                    "value": [
                        {
                            "value": str(self.scim_user.scim_external_id),
                            "display": self.scim_user.username,
                        }
                    ],
                }
            ],
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        membership = UserGroup.objects.get(
            user=self.scim_user,
            group=self.group,
        )

        self.assertIsNone(membership.periode.upper)

    def test_entra_id_remove_group_member(self):
        """
        Simulates:
        PATCH /scim/v2/Groups/{id}
        remove member
        """

        UserGroup.objects.create(
            user=self.scim_user,
            group=self.group,
            periode=DateRange(
                timezone.now().date() - timedelta(days=30),
                None,
            ),
        )

        url = reverse(
            "scim:group-detail",
            kwargs={"uuid": self.group.scim_external_id},
        )

        payload = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
            "Operations": [
                {
                    "op": "Remove",
                    "path": "members",
                    "value": [
                        {
                            "value": str(self.scim_user.scim_external_id),
                        }
                    ],
                }
            ],
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        membership = UserGroup.objects.get(
            user=self.scim_user,
            group=self.group,
        )

        self.assertIsNotNone(membership.periode.upper)

    def test_entra_id_get_group_returns_membership_dates(self):
        """
        Simulates:
        GET /scim/v2/Groups/{id}
        """

        start_date = timezone.now().date() - timedelta(days=5)

        UserGroup.objects.create(
            user=self.scim_user,
            group=self.group,
            periode=DateRange(
                start_date,
                None,
            ),
        )

        url = reverse(
            "scim:group-detail",
            kwargs={"uuid": self.group.scim_external_id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        members = response.data["members"]

        self.assertEqual(len(members), 1)

        member = members[0]

        self.assertEqual(
            member["value"],
            str(self.scim_user.scim_external_id),
        )

        self.assertEqual(
            member["startDate"],
            start_date.isoformat(),
        )

        self.assertIsNone(member["endDate"])
