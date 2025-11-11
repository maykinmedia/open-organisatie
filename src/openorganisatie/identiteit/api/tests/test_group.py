from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openorganisatie.identiteit.models.factories.group import GroupFactory

from .api_testcase import APITestCase


class GroupAPITests(APITestCase):
    def test_list_groups(self):
        url = reverse("identiteit_api:group-list")
        GroupFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for group in data:
            self.assertIn("scimExternalId", group)
            self.assertIn("naam", group)
            self.assertIn("beschrijving", group)

    def test_group_detail(self):
        group = GroupFactory()

        detail_url = reverse(
            "identiteit_api:group-detail",
            kwargs={"scim_external_id": group.scim_external_id},
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["scimExternalId"], str(group.scim_external_id))
        self.assertEqual(data["naam"], group.name)
        self.assertEqual(data["beschrijving"], group.description)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("identiteit_api:group-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_naam(self):
        group1 = GroupFactory(name="Finance Group")
        GroupFactory(name="HR Group")

        url = reverse("identiteit_api:group-list")
        response = self.client.get(url, {"naam": "finance"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["naam"], group1.name)
