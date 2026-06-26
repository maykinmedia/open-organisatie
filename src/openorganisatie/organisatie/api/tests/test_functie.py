from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.timezone import make_aware

from psycopg.types.range import DateRange
from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from openorganisatie.organisatie.models.factories.functie import (
    FunctieFactory,
    FunctieTeamFactory,
    FunctieTypeFactory,
    OrganisatorischeEenheidFunctieFactory,
)
from openorganisatie.organisatie.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.organisatie.models.factories.team import TeamFactory

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

    def test_create_functie_with_team(self):
        url = reverse("organisatie_api:functie-list")
        team = TeamFactory()

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-12-31",
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(response.data["teams"]), 1)
        self.assertEqual(
            response.data["teams"][0]["team"]["uuid"],
            str(team.uuid),
        )

    def test_create_functie_with_organisatorische_eenheid(self):
        url = reverse("organisatie_api:functie-list")

        oe = OrganisatorischeEenheidFactory()
        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "organisatorischeEenhedenInput": [
                {
                    "organisatorischeEenheidUuid": str(oe.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-12-31",
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(response.data["organisatorische_eenheden"]), 1)
        self.assertEqual(
            response.data["organisatorische_eenheden"][0]["organisatorische_eenheid"][
                "uuid"
            ],
            str(oe.uuid),
        )

    def test_create_functie_with_multiple_teams_and_oe(self):
        url = reverse("organisatie_api:functie-list")

        team1 = TeamFactory()
        team2 = TeamFactory()
        oe1 = OrganisatorischeEenheidFactory()

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team1.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-06-01",
                    },
                },
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-06-02",
                        "einde_geldigheid": "2025-06-05",
                    },
                },
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-07-02",
                        "einde_geldigheid": None,
                    },
                },
            ],
            "organisatorischeEenhedenInput": [
                {
                    "organisatorischeEenheidUuid": str(oe1.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(response.data["teams"]), 2)
        self.assertEqual(len(response.data["organisatorische_eenheden"]), 1)

    def test_create_functie_with_open_ended_team(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNone(
            response.data["teams"][0]["geldigheid"][0]["einde_geldigheid"]
        )

    def test_create_functie_team_overlap_should_fail(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        FunctieTeamFactory(
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), None),
        )

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-06-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_functie_team_overlap_exact_same_geldigheid_should_fail(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        FunctieTeamFactory(
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-06-01",
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_functie_team_partial_overlap_should_fail(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        FunctieTeamFactory(
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-05-01",
                        "einde_geldigheid": "2025-07-01",
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_functie_team_open_ended_overlap_should_fail(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        FunctieTeamFactory(
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), None),
        )

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_functie_oe_overlap_should_fail(self):
        url = reverse("organisatie_api:functie-list")

        oe = OrganisatorischeEenheidFactory()

        OrganisatorischeEenheidFunctieFactory(
            organisatorische_eenheid=oe,
            geldigheid=DateRange(date(2025, 1, 1), None),
        )

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-01-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "organisatorischeEenhedenInput": [
                {
                    "organisatorischeEenheidUuid": str(oe.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_functie_with_vervanger(self):
        vervanger = FunctieFactory()

        url = reverse("organisatie_api:functie-list")

        data = {
            "functieOmschrijving": "Functie met vervanger",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "vervanger": str(vervanger.uuid),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        functie = Functie.objects.get(uuid=response.data["uuid"])
        self.assertEqual(functie.vervanger, vervanger)

    def test_list_functies(self):
        url = reverse("organisatie_api:functie-list")
        team = TeamFactory()
        oe = OrganisatorischeEenheidFactory()
        FunctieFactory.create_batch(
            3,
            teams=[team],
            organisatorische_eenheden=[oe],
        )

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

    def test_update_functie_vervanger(self):
        functie = FunctieFactory()
        vervanger = FunctieFactory()

        url = reverse(
            "organisatie_api:functie-detail",
            kwargs={"uuid": functie.uuid},
        )

        data = {
            "functieOmschrijving": "Updated Functie",
            "startdatum": "2025-12-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "vervanger": str(vervanger.uuid),
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(functie.functie_omschrijving, "Updated Functie")
        self.assertEqual(functie.vervanger, vervanger)

    def test_patch_functie_vervanger(self):
        functie = FunctieFactory()
        vervanger1 = FunctieFactory()
        vervanger2 = FunctieFactory()

        functie.vervanger = vervanger1
        functie.save()

        url = reverse(
            "organisatie_api:functie-detail",
            kwargs={"uuid": functie.uuid},
        )

        response = self.client.patch(
            url,
            {"vervanger": str(vervanger2.uuid)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertEqual(functie.vervanger, vervanger2)

    def test_patch_remove_vervanger(self):
        functie = FunctieFactory()
        vervanger = FunctieFactory()

        functie.vervanger = vervanger
        functie.save()

        url = reverse(
            "organisatie_api:functie-detail",
            kwargs={"uuid": functie.uuid},
        )

        response = self.client.patch(
            url,
            {"vervanger": None},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        self.assertIsNone(functie.vervanger)

    def test_create_functie_cannot_be_own_vervanger(self):
        url = reverse("organisatie_api:functie-list")

        data = {
            "functieOmschrijving": "Self vervanger test",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
        }

        response = self.client.post(url, data)

        functie_uuid = response.data["uuid"]

        response = self.client.patch(
            reverse("organisatie_api:functie-detail", kwargs={"uuid": functie_uuid}),
            {"vervanger": functie_uuid},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_prevent_self_parenting(self):
        functie = FunctieFactory()
        functie.vervanger = functie
        with self.assertRaises(ValidationError) as val:
            functie.clean()
        self.assertIn(
            "vervanger",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een vervanger kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["vervanger"][0],
        )

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

    def test_update_functie_replaces_teams(self):
        team1 = TeamFactory()
        team2 = TeamFactory()

        functie = FunctieFactory(teams=[team1])

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "startdatum": functie.startdatum.isoformat(),
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()

        rels = functie.functieteam_set.all()
        self.assertEqual(rels.count(), 2)
        self.assertEqual(rels.first().team_id, team1.id)

    def test_patch_functie_patch_teams(self):
        team1 = TeamFactory()
        team2 = TeamFactory()

        functie = FunctieFactory(teams=[team1])

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "startdatum": functie.startdatum.isoformat(),
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()
        rels = functie.functieteam_set.all()

        self.assertEqual(rels.count(), 2)
        self.assertEqual(rels.first().team_id, team1.id)

    def test_update_functie_replaces_organisatorische_eenheden(self):
        oe1 = OrganisatorischeEenheidFactory()
        oe2 = OrganisatorischeEenheidFactory()

        functie = FunctieFactory(organisatorische_eenheden=[oe1])

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "startdatum": functie.startdatum.isoformat(),
            "functietypeUuid": str(self.functie_type.uuid),
            "organisatorischeEenhedenInput": [
                {
                    "organisatorischeEenheidUuid": str(oe2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()

        rels = functie.organisatorischeeenheidfunctie_set.all()
        self.assertEqual(rels.count(), 2)
        self.assertEqual(rels.first().organisatorische_eenheid_id, oe1.id)

    def test_patch_functie_patch_organisatorische_eenheden(self):
        oe1 = OrganisatorischeEenheidFactory()
        oe2 = OrganisatorischeEenheidFactory()

        functie = FunctieFactory(organisatorische_eenheden=[oe1])

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "startdatum": functie.startdatum.isoformat(),
            "functietypeUuid": str(self.functie_type.uuid),
            "organisatorischeEenhedenInput": [
                {
                    "organisatorischeEenheidUuid": str(oe2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-02-01",
                        "einde_geldigheid": None,
                    },
                }
            ],
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie.refresh_from_db()

        rels = functie.organisatorischeeenheidfunctie_set.all()
        self.assertEqual(rels.count(), 2)
        self.assertEqual(rels.first().organisatorische_eenheid_id, oe1.id)

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

    def test_filter_functie_external_id(self):
        functie1 = FunctieFactory()
        FunctieFactory()

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"external_id": str(functie1.external_id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["external_id"], str(functie1.external_id)
        )

    def test_filter_team_uuid(self):
        team1 = TeamFactory()
        team2 = TeamFactory()

        functie1 = FunctieFactory(teams=[team1])
        FunctieFactory(teams=[team2])

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(url, {"team_uuid": str(team1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_filter_multiple_team_uuids(self):
        team1 = TeamFactory()
        team2 = TeamFactory()
        team3 = TeamFactory()

        FunctieFactory(teams=[team1])
        FunctieFactory(teams=[team2])
        FunctieFactory(teams=[team3])

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(
            url,
            {
                "team_uuid": f"{team1.uuid},{team2.uuid}",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_organisatorische_eenheid_uuid(self):
        oe1 = OrganisatorischeEenheidFactory()
        oe2 = OrganisatorischeEenheidFactory()

        functie1 = FunctieFactory(organisatorische_eenheden=[oe1])
        FunctieFactory(organisatorische_eenheden=[oe2])

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(
            url, {"organisatorische_eenheid_uuid": str(oe1.uuid)}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(functie1.uuid))

    def test_filter_multiple_organisatorische_eenheid_uuids(self):
        oe1 = OrganisatorischeEenheidFactory()
        oe2 = OrganisatorischeEenheidFactory()
        oe3 = OrganisatorischeEenheidFactory()

        FunctieFactory(organisatorische_eenheden=[oe1])
        FunctieFactory(organisatorische_eenheden=[oe2])
        FunctieFactory(organisatorische_eenheden=[oe3])

        url = reverse("organisatie_api:functie-list")
        response = self.client.get(
            url,
            {
                "organisatorische_eenheid_uuid": f"{oe1.uuid},{oe2.uuid}",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

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

    def test_filter_active_on_team_date(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        functie = FunctieFactory()

        FunctieTeamFactory(
            functie=functie,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )
        FunctieTeamFactory(
            geldigheid=DateRange(date(2026, 1, 1), date(2026, 6, 1)),
        )

        response = self.client.get(url, {"actief_op_team": "2025-03-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        self.assertEqual(response.data["results"][0]["uuid"], str(functie.uuid))

    def test_filter_active_on_team_date_outside_range(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        functie = FunctieFactory()

        FunctieTeamFactory(
            functie=functie,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        response = self.client.get(url, {"actief_op_team": "2025-07-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_filter_active_on_team_date_open_ended(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        functie = FunctieFactory()

        FunctieTeamFactory(
            functie=functie,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), None),
        )

        response = self.client.get(url, {"actief_op_team": "2030-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        uuids = {f["uuid"] for f in response.data["results"]}
        self.assertIn(str(functie.uuid), uuids)

    def test_filter_active_on_team_date_multiple_functions(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        functie1 = FunctieFactory()
        functie2 = FunctieFactory()

        FunctieTeamFactory(
            functie=functie1,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        FunctieTeamFactory(
            functie=functie2,
            team=team,
            geldigheid=DateRange(date(2026, 1, 1), date(2026, 6, 1)),
        )

        response = self.client.get(url, {"actief_op_team": "2025-03-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        uuids = {f["uuid"] for f in response.data["results"]}
        self.assertIn(str(functie1.uuid), uuids)

    def test_filter_active_on_team_date_multiple_functions_same_team(self):
        url = reverse("organisatie_api:functie-list")

        team = TeamFactory()

        functie1 = FunctieFactory()
        functie2 = FunctieFactory()

        FunctieTeamFactory(
            functie=functie1,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        FunctieTeamFactory(
            functie=functie2,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2026, 6, 1)),
        )

        response = self.client.get(url, {"actief_op_team": "2025-03-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        uuids = {f["uuid"] for f in response.data["results"]}
        self.assertIn(str(functie1.uuid), uuids)

    def test_filter_active_on_team_date_multiple_teams_same_functie(self):
        url = reverse("organisatie_api:functie-list")

        team1 = TeamFactory()
        team2 = TeamFactory()

        functie = FunctieFactory()

        FunctieTeamFactory(
            functie=functie,
            team=team1,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        FunctieTeamFactory(
            functie=functie,
            team=team2,
            geldigheid=DateRange(date(2025, 2, 1), date(2025, 5, 1)),
        )

        response = self.client.get(url, {"actief_op_team": "2025-03-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        self.assertEqual(response.data["results"][0]["uuid"], str(functie.uuid))

    def test_put_team_geldigheid_(self):
        url = reverse("organisatie_api:functie-list")
        team = TeamFactory()
        team2 = TeamFactory()

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        # "einde_geldigheid": "2025-12-31",
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        uuid = response.data["uuid"]

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": uuid})

        data = {
            "functieOmschrijving": "update",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-06-01",
                    },
                },
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-06-01",
                        "einde_geldigheid": "2025-08-01",
                    },
                },
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-06-01",
                    },
                },
                {
                    "teamUuid": str(team2.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-06-01",
                        "einde_geldigheid": "2025-08-01",
                    },
                },
            ],
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie = Functie.objects.get(uuid=uuid)
        self.assertEqual(functie.functie_omschrijving, "update")
        self.assertEqual(functie.functieteam_set.count(), 4)

    def test_close_team_geldigheid(self):
        team = TeamFactory()
        functie = FunctieFactory()

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        rel = FunctieTeamFactory(
            functie=functie,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), None),
        )

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "startdatum": functie.startdatum.isoformat(),
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        "einde_geldigheid": "2025-06-01",
                    },
                }
            ],
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rel.refresh_from_db()
        self.assertEqual(rel.geldigheid.upper, date(2025, 6, 1))

    def test_update_empty_list_team_geldigheid(self):
        url = reverse("organisatie_api:functie-list")
        team = TeamFactory()

        data = {
            "functieOmschrijving": "Test functie",
            "startdatum": "2025-11-01",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-01-01",
                        # "einde_geldigheid": "2025-12-31",
                    },
                }
            ],
        }

        response = self.client.post(url, data)

        uuid = response.data["uuid"]

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": uuid})

        data = {
            "functieOmschrijving": "update",
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [],
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        functie = Functie.objects.get(uuid=uuid)
        self.assertEqual(functie.functie_omschrijving, "update")

        self.assertEqual(functie.functieteam_set.count(), 1)

        relation = functie.functieteam_set.first()
        self.assertEqual(str(relation.team.uuid), str(team.uuid))

    def test_patch_cannot_introduce_overlap(self):
        team = TeamFactory()

        functie = FunctieFactory()

        FunctieTeamFactory(
            functie=functie,
            team=team,
            geldigheid=DateRange(date(2025, 1, 1), date(2025, 6, 1)),
        )

        url = reverse("organisatie_api:functie-detail", kwargs={"uuid": functie.uuid})

        data = {
            "functieOmschrijving": functie.functie_omschrijving,
            "functietypeUuid": str(self.functie_type.uuid),
            "teamsInput": [
                {
                    "teamUuid": str(team.uuid),
                    "geldigheid": {
                        "begin_geldigheid": "2025-05-01",
                        "einde_geldigheid": "2025-07-01",
                    },
                }
            ],
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
