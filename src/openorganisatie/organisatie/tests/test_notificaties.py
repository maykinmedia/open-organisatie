import uuid
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse

from freezegun import freeze_time
from notifications_api_common.models import NotificationsConfig
from rest_framework import status
from zgw_consumers.constants import APITypes
from zgw_consumers.models import Service

from openorganisatie.organisatie.models.factories.medewerker import (
    MedewerkerFactory,
)

from ..api.tests.api_testcase import APITestCase


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
class SendNotificationMedewerkerTestCase(NotificationsConfigTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.medewerker = MedewerkerFactory.create()
        cls.list_url = reverse("organisatie_api:medewerker-list")
        cls.detail_url = reverse(
            "organisatie_api:medewerker-detail",
            kwargs={"uuid": str(cls.medewerker.uuid)},
        )

        cls.data = {
            "uuid": str(uuid.uuid4()),
            "medewerkerId": "m12345",
            "voornaam": "Pieter",
            "achternaam": "Jansen",
            "emailadres": "pieter@gmail.com",
            "telefoonnummer": "0612345678",
        }

    def test_send_notification_create_medewerker(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.list_url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        m.assert_called_with(
            {
                "kanaal": "medewerkers",
                "hoofdObject": data["url"],
                "resource": "medewerker",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "uuid": str(data["uuid"]),
                    "medewerkerId": "m12345",
                    "voornaam": "Pieter",
                    "achternaam": "Jansen",
                    "emailadres": "pieter@gmail.com",
                },
            }
        )

    def test_send_notification_update_medewerker(self, m):
        """Test that a notification is sent on medewerker update."""
        updated_data = {
            "uuid": str(self.medewerker.uuid),
            "medewerkerId": "m54321",
            "voornaam": "Pieter",
            "achternaam": "Jansen",
            "emailadres": "pieter@gmail.com",
            "telefoonnummer": "0612345678",
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.put(self.detail_url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        m.assert_called_with(
            {
                "kanaal": "medewerkers",
                "hoofdObject": data["url"],
                "resource": "medewerker",
                "resourceUrl": data["url"],
                "actie": "update",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "uuid": str(data["uuid"]),
                    "medewerkerId": "m54321",
                    "voornaam": "Pieter",
                    "achternaam": "Jansen",
                    "emailadres": "pieter@gmail.com",
                },
            }
        )

        self.medewerker.refresh_from_db()
        self.assertEqual(self.medewerker.medewerker_id, "m54321")

    def test_send_notification_partial_update_medewerker(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(self.detail_url, {"voornaam": "Jan"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        m.assert_called_with(
            {
                "kanaal": "medewerkers",
                "hoofdObject": data["url"],
                "resource": "medewerker",
                "resourceUrl": data["url"],
                "actie": "partial_update",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "uuid": str(self.medewerker.uuid),
                    "medewerkerId": self.medewerker.medewerker_id,
                    "voornaam": "Jan",
                    "achternaam": self.medewerker.achternaam,
                    "emailadres": self.medewerker.emailadres,
                },
            }
        )

    def test_send_notification_delete_medewerker(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        m.assert_called_with(
            {
                "kanaal": "medewerkers",
                "hoofdObject": f"http://testserver{self.detail_url}",
                "resource": "medewerker",
                "resourceUrl": f"http://testserver{self.detail_url}",
                "actie": "destroy",
                "aanmaakdatum": "2025-10-09T02:00:00+02:00",
                "kenmerken": {
                    "uuid": str(self.medewerker.uuid),
                    "medewerkerId": self.medewerker.medewerker_id,
                    "voornaam": self.medewerker.voornaam,
                    "achternaam": self.medewerker.achternaam,
                    "emailadres": self.medewerker.emailadres,
                },
            }
        )
