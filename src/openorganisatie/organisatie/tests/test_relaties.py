from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from psycopg.types.range import DateRange

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)
from openorganisatie.organisatie.models.factories.team import TeamFactory

from ..models.relaties import (
    FunctieTeam,
    OrganisatorischeEenheidFunctie,
)


class FunctieTeamCleanTests(TestCase):
    def test_clean_overlapping_geldigheid(self):
        functie = FunctieFactory()
        team = TeamFactory()

        FunctieTeam.objects.create(
            functie=functie,
            team=team,
            geldigheid=DateRange(
                lower=date(2025, 1, 1),
                upper=date(2025, 12, 31),
            ),
        )

        relatie = FunctieTeam(
            functie=functie,
            team=team,
            geldigheid=DateRange(
                lower=date(2025, 6, 1),
                upper=date(2026, 1, 1),
            ),
        )

        with self.assertRaises(ValidationError) as cm:
            relatie.clean()

        self.assertEqual(
            cm.exception.message_dict["geldigheid"],
            ["Deze geldigheid overlapt met een bestaande toewijzing."],
        )


class OrganisatorischeEenheidFunctieCleanTests(TestCase):
    def test_clean_overlapping_geldigheid(self):
        functie = FunctieFactory()
        organisatorische_eenheid = OrganisatorischeEenheidFactory()

        OrganisatorischeEenheidFunctie.objects.create(
            functie=functie,
            organisatorische_eenheid=organisatorische_eenheid,
            geldigheid=DateRange(
                lower=date(2025, 1, 1),
                upper=date(2025, 12, 31),
            ),
        )

        relatie = OrganisatorischeEenheidFunctie(
            functie=functie,
            organisatorische_eenheid=organisatorische_eenheid,
            geldigheid=DateRange(
                lower=date(2025, 6, 1),
                upper=date(2026, 1, 1),
            ),
        )

        with self.assertRaises(ValidationError) as cm:
            relatie.clean()

        self.assertEqual(
            cm.exception.message_dict["geldigheid"],
            ["Deze geldigheid overlapt met een bestaande toewijzing."],
        )
