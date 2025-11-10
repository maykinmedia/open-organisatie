import uuid
from unittest.mock import patch

from django.test import RequestFactory, override_settings
from django.urls import reverse

from freezegun import freeze_time
from notifications_api_common.models import NotificationsConfig
from rest_framework import status
from zgw_consumers.constants import APITypes
from zgw_consumers.models import Service

from openorganisatie.identiteit.adapters import UserAdapter
from openorganisatie.identiteit.models.user import User

from ..api.tests.api_testcase import APITestCaseBearer


class NotificationsConfigTestCase:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        service, _ = Service.objects.update_or_create(
            api_root="https://notificaties-api.vng.cloud/api/v1/",
            defaults=dict(
                api_type=APITypes.nrc,
                client_id="test",
                secret="test",
                user_id="test",
                user_representation="Test",
            ),
        )
        config = NotificationsConfig.get_solo()
        config.notifications_api_service = service
        config.save()


@freeze_time("2025-10-09T00:00:00Z")
@patch("notifications_api_common.viewsets.send_notification.delay")
@override_settings(NOTIFICATIONS_DISABLED=False)
class SendNotificationUserTestCase(NotificationsConfigTestCase, APITestCaseBearer):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.existing_user = User.objects.create(
            scim_external_id=str(uuid.uuid4()),
            username="existing",
            first_name="Existing",
            last_name="User",
            email="existing@gmail.com",
            is_active=True,
        )

        cls.list_url = reverse("scim:users")
        cls.detail_url = reverse(
            "scim:user-detail", kwargs={"uuid": cls.existing_user.scim_external_id}
        )
        factory = RequestFactory()
        cls.request = factory.get(cls.detail_url)
        cls.adapter = UserAdapter(cls.existing_user, request=cls.request)

        cls.data = {
            "externalId": str(uuid.uuid4()),
            "userName": "Bob",
            "emails": [{"value": "Bob@gmail.com"}],
            "name": {"givenName": "Bob", "familyName": "Jansen"},
            "active": True,
        }

    def test_send_notification_create_user(self, m):
        """A notification is sent when a new SCIM user is created."""
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                self.list_url, self.data, content_type="application/json"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        m.assert_called_with(
            {
                "kanaal": "users",
                "hoofdObject": data["url"],
                "resource": "user",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "scimExternalId": str(data["externalId"]),
                    "username": "Bob",
                    "email": "Bob@gmail.com",
                },
            }
        )

    def test_send_notification_update_user(self, m):
        """A notification is sent when a SCIM user is updated."""
        operations = [
            {"op": "replace", "path": "name.givenName", "value": "Peter"},
            {"op": "replace", "path": "name.familyName", "value": "Jansen"},
            {
                "op": "replace",
                "path": 'emails[type eq "work"].value',
                "value": "test@gmail.com",
            },
            {"op": "replace", "path": "active", "value": True},
        ]

        payload = {"Operations": operations}

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(
                self.detail_url, data=payload, content_type="application/json"
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        m.assert_called_with(
            {
                "kanaal": "users",
                "hoofdObject": data["meta"]["location"],
                "resource": "user",
                "resourceUrl": data["meta"]["location"],
                "actie": "update",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "scimExternalId": data["externalId"],
                    "username": data["userName"],
                    "email": data["emails"][0]["value"],
                },
            }
        )
