from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status

from openorganisatie.organisatie.api.tests.api_testcase import APITestCase
from openorganisatie.organisatie.metrics import (
    medewerkers_create_counter,
    medewerkers_delete_counter,
    medewerkers_update_counter,
)
from openorganisatie.organisatie.models.factories.medewerker import (
    MedewerkerFactory,
)


class MedewerkerMetricsTests(APITestCase):
    def setUp(self):
        super().setUp()

        self.data = {
            "voornaam": "Test",
            "achternaam": "User",
            "emailadres": "test@example.com",
            "medewerker_id": "ABC123",
        }

    @patch.object(
        medewerkers_create_counter, "add", wraps=medewerkers_create_counter.add
    )
    def test_medewerker_create_counter(self, mock_add: MagicMock):
        response = self.client.post(
            reverse("organisatie_api:medewerker-list"),
            self.data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_add.assert_called_once_with(1)

    @patch.object(
        medewerkers_update_counter, "add", wraps=medewerkers_update_counter.add
    )
    def test_medewerker_update_counter(self, mock_add: MagicMock):
        medewerker = MedewerkerFactory.create()

        update_data = {
            "voornaam": "Updated",
            "achternaam": medewerker.achternaam,
            "emailadres": medewerker.emailadres,
            "medewerker_id": medewerker.medewerker_id,
        }

        response = self.client.put(
            reverse(
                "organisatie_api:medewerker-detail",
                kwargs={"uuid": str(medewerker.uuid)},
            ),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_add.assert_called_once_with(1)

    @patch.object(
        medewerkers_delete_counter, "add", wraps=medewerkers_delete_counter.add
    )
    def test_medewerker_delete_counter(self, mock_add: MagicMock):
        medewerker = MedewerkerFactory.create()

        response = self.client.delete(
            reverse(
                "organisatie_api:medewerker-detail",
                kwargs={"uuid": str(medewerker.uuid)},
            )
        )

        self.assertIn(
            response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK)
        )
        mock_add.assert_called_once_with(1)
