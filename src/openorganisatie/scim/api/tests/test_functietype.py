from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.scim.models.factories.functie import FunctieTypeFactory

from ...models import FunctieType
from .api_testcase import APITestCase


class FunctieTypeAPITests(APITestCase):
    def test_list_functietypes(self):
        url = reverse("scim_api:functietype-list")
        FunctieTypeFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 3)
        for functietype in data["results"]:
            self.assertIn("uuid", functietype)
            self.assertIn("naam", functietype)
            self.assertIn("slug", functietype)

    def test_read_functietype_detail(self):
        functietype = FunctieTypeFactory()
        detail_url = reverse(
            "scim_api:functietype-detail", kwargs={"uuid": functietype.uuid}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(functietype.uuid))
        self.assertEqual(data["naam"], functietype.naam)
        self.assertEqual(data["slug"], functietype.slug)

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("scim_api:functietype-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_naam(self):
        ft1 = FunctieTypeFactory(naam="Manager HR")
        FunctieTypeFactory(naam="Developer")

        url = reverse("scim_api:functietype-list")
        response = self.client.get(url, {"naam": "Manager HR"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(ft1.uuid))

    def test_filter_slug(self):
        ft1 = FunctieTypeFactory(slug="finance")
        FunctieTypeFactory(slug="marketing")

        url = reverse("scim_api:functietype-list")
        response = self.client.get(url, {"slug": "finance"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(ft1.uuid))

    def test_history(self):
        url = reverse("scim_api:functietype-list")
        data = {"naam": "abc", "slug": "abc"}

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            functietype = FunctieType.objects.get()
            self.assertEqual(Version.objects.get_for_object(functietype).count(), 1)

        detail_url = reverse(
            "scim_api:functietype-detail", kwargs={"uuid": functietype.uuid}
        )

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functietype).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"naam": "defg"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functietype).count(), 3)
