import uuid
from datetime import datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.scim.models.factories.group import GroupFactory
from openorganisatie.scim.models.factories.user import UserFactory

from .api_testcase import APITestCase


class UserAPITests(APITestCase):
    def test_list_userss(self):
        url = reverse("scim_api:user-list")
        UserFactory.create_batch(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_user_detail(self):
        user = UserFactory()

        detail_url = reverse(
            "scim_api:user-detail",
            kwargs={"scim_external_id": str(user.scim_external_id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["username"], str(user.username))
        self.assertEqual(data["voornaam"], user.first_name)
        self.assertEqual(data["achternaam"], user.last_name)
        self.assertEqual(data["emailadres"], user.email)

    def test_authentication_required(self):
        client = APIClient()

        url = reverse("scim_api:user-list")
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_groups(self):
        group1 = GroupFactory(scim_external_id=str(uuid.uuid4()))
        group2 = GroupFactory(scim_external_id=str(uuid.uuid4()))

        m1 = UserFactory()
        m1.groups.add(group1)

        UserFactory().groups.add(group2)

        url = reverse("scim_api:user-list")
        response = self.client.get(url, {"groups": [group1.scim_external_id]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_datum_toegevoegd(self):
        m1 = UserFactory(date_joined=make_aware(datetime(2025, 1, 1)))
        UserFactory(date_joined=make_aware(datetime(2026, 1, 1)))

        url = reverse("scim_api:user-list")
        response = self.client.get(url, {"datum_toegevoegd": "2025-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["datum_toegevoegd"], m1.date_joined.isoformat()
        )
