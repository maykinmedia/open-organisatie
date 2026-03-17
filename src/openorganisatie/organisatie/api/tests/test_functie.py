from datetime import date, datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.functie import (
    FunctieFactory,
    FunctieTypeFactory,
)

from ...models import Functie
from .api_testcase import APITestCase


class FunctieAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.functie_type = FunctieTypeFactory()

    def test_create_functie(self):
        url = reverse("organisatie_api:functie-list")
        data = {
            "functieOmschrijving": "Nieuwe Functie",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        functie = Functie.objects.get(uuid=response.data["uuid"])
        self.assertEqual(functie.functie_omschrijving, data["functieOmschrijving"])
        self.assertEqual(functie.startdatum.isoformat(), data["startdatum"])

    def test_list_functies(self):
        url = reverse("organisatie_api:functie-list")
        FunctieFactory.create_batch(3)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 3)
        for functie in data["results"]:
            self.assertIn("uuid", functie)
            self.assertIn("functieOmschrijving", functie)
            self.assertIn("startdatum", functie)

    def test_read_functie_detail(self):
        type1 = FunctieTypeFactory()
        functie = FunctieFactory(functie_type=type1)
        detail_url = reverse(
            "organisatie_api:functie-detail", kwargs={"uuid": functie.uuid}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["uuid"], str(functie.uuid))
        self.assertEqual(data["functieOmschrijving"], functie.functie_omschrijving)
        self.assertEqual(data["startdatum"], functie.startdatum.isoformat())

    def test_update_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse(
            "organisatie_api:functie-detail", kwargs={"uuid": functie.uuid}
        )

        data = {
            "functieOmschrijving": "Bijgewerkte Functie",
            "startdatum": "2025-12-01",
            "functietypeUuid": str(self.functie_type.uuid),
        }
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(functie.functie_omschrijving, data["functieOmschrijving"])
        self.assertEqual(functie.startdatum.isoformat(), data["startdatum"])

    def test_partial_update_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse(
            "organisatie_api:functie-detail", kwargs={"uuid": functie.uuid}
        )

        patch_data = {"functieOmschrijving": "Gedeeltelijk Bijgewerkt"}
        response = self.client.patch(detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(
            functie.functie_omschrijving, patch_data["functieOmschrijving"]
        )

    def test_delete_functie(self):
        functie = FunctieFactory(functie_type=self.functie_type)
        detail_url = reverse(
            "organisatie_api:functie-detail", kwargs={"uuid": functie.uuid}
        )

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Functie.objects.filter(uuid=functie.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("organisatie_api:functie-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_functie_omschrijving(self):
        functie1 = FunctieFactory(functie_omschrijving="Software Engineer")
        FunctieFactory(functie_omschrijving="Data Scientist")

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"functie_omschrijving": "Software Engineer"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_filter_functie_type_uuid(self):
        type1 = FunctieTypeFactory()
        type2 = FunctieTypeFactory()

        functie1 = FunctieFactory(functie_type=type1)
        FunctieFactory(functie_type=type2)

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"functie_type_uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_history(self):
        url = reverse("organisatie_api:functie-list")
        data = {
            "functieOmschrijving": "1234",
            "startdatum": "2025-10-10",
            "functietypeUuid": str(FunctieTypeFactory.create().uuid),
        }

        with self.subTest("create"):
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            functie = Functie.objects.get()
            self.assertEqual(Version.objects.get_for_object(functie).count(), 1)

        detail_url = reverse(
            "organisatie_api:functie-detail", kwargs={"uuid": functie.uuid}
        )

        with self.subTest("update"):
            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functie).count(), 2)

        with self.subTest("partial update"):
            response = self.client.patch(detail_url, {"functieOmschrijving": "abc"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Version.objects.get_for_object(functie).count(), 3)

    def test_filter_startdatum(self):
        f1 = FunctieFactory(startdatum=date(2025, 1, 1))
        FunctieFactory(startdatum=date(2026, 1, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"startdatum": "2025-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], f1.startdatum.isoformat()
        )

    def test_filter_startdatum_gte(self):
        FunctieFactory(startdatum=date(2024, 12, 31))
        f2 = FunctieFactory(startdatum=date(2025, 2, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"startdatum__gte": "2025-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], f2.startdatum.isoformat()
        )

    def test_filter_startdatum_lte(self):
        f1 = FunctieFactory(startdatum=date(2024, 12, 31))
        FunctieFactory(startdatum=date(2025, 3, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"startdatum__lte": "2025-01-31"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["startdatum"], f1.startdatum.isoformat()
        )

    def test_filter_einddatum(self):
        f1 = FunctieFactory(einddatum=date(2025, 1, 1))
        FunctieFactory(einddatum=date(2026, 1, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"einddatum": "2025-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], f1.einddatum.isoformat()
        )

    def test_filter_einddatum_gte(self):
        FunctieFactory(einddatum=date(2024, 12, 31))
        f2 = FunctieFactory(einddatum=date(2025, 2, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"einddatum__gte": "2025-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], f2.einddatum.isoformat()
        )

    def test_filter_einddatum_lte(self):
        f1 = FunctieFactory(einddatum=date(2024, 12, 31))
        FunctieFactory(einddatum=date(2025, 3, 1))

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"einddatum__lte": "2025-01-31"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["einddatum"], f1.einddatum.isoformat()
        )

    def test_filter_wijzigingsdatum(self):
        dt1 = make_aware(datetime(2025, 1, 1, 10, 30))
        dt2 = make_aware(datetime(2026, 1, 1, 12, 0))
        f1 = FunctieFactory(wijzigingsdatum=dt1)
        FunctieFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"wijzigingsdatum": dt1.isoformat()})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            f1.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_gte(self):
        make_aware(datetime(2024, 12, 31, 9, 0))
        dt2 = make_aware(datetime(2025, 2, 1, 15, 45))
        f2 = FunctieFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(
            url, {"wijzigingsdatum__gte": "2025-01-01T00:00:00Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            f2.wijzigingsdatum.isoformat(),
        )

    def test_filter_wijzigingsdatum_lte(self):
        dt1 = make_aware(datetime(2024, 12, 31, 8, 0))
        dt2 = make_aware(datetime(2025, 3, 1, 12, 0))
        f1 = FunctieFactory(wijzigingsdatum=dt1)
        FunctieFactory(wijzigingsdatum=dt2)

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(
            url, {"wijzigingsdatum__lte": "2025-01-31T23:59:59Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["wijzigingsdatum"],
            f1.wijzigingsdatum.isoformat(),
        )
