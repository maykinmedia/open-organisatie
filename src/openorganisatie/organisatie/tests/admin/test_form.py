from datetime import date

from django.test import TestCase

from psycopg.types.range import DateRange

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.team import TeamFactory

from ...admin.functie import TeamFunctieInlineForm


class FunctieTeamInlineFormTests(TestCase):
    def test_form_valid(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = TeamFunctieInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "geldigheid_0": "2025-01-01",
                "geldigheid_1": "2025-12-31",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

        geldigheid = form.cleaned_data["geldigheid"]

        self.assertEqual(geldigheid.lower, date(2025, 1, 1))
        self.assertEqual(geldigheid.upper, date(2025, 12, 31))

    def test_form_without_periode(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = TeamFunctieInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "geldigheid_0": "",
                "geldigheid_1": "",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertFalse(form.is_valid())
        self.assertIn("geldigheid", form.errors)

    def test_form_invalid_startdatum(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = TeamFunctieInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "geldigheid_0": "invalid-date",
                "geldigheid_1": "2025-12-31",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("geldigheid", form.errors)

    def test_form_invalid_einddatum(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = TeamFunctieInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "geldigheid_0": "2025-01-01",
                "geldigheid_1": "invalid-date",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("geldigheid", form.errors)

    def test_widget_decompress(self):
        widget = TeamFunctieInlineForm.base_fields["geldigheid"].widget

        value = DateRange(
            lower=date(2025, 1, 1),
            upper=date(2025, 12, 31),
        )

        decompressed = widget.decompress(value)

        self.assertEqual(
            decompressed,
            [
                date(2025, 1, 1),
                date(2025, 12, 31),
            ],
        )

    def test_widget_decompress_empty_value(self):
        widget = TeamFunctieInlineForm.base_fields["geldigheid"].widget

        decompressed = widget.decompress(None)

        self.assertEqual(decompressed, [None, None])

    def test_widget_contains_placeholders(self):
        form = TeamFunctieInlineForm()

        html = str(form["geldigheid"])

        self.assertIn("Begin geldigheid", html)
        self.assertIn("Einde geldigheid", html)

    def test_widget_uses_admin_date_widget(self):
        form = TeamFunctieInlineForm()

        html = str(form["geldigheid"])

        self.assertIn("vDateField", html)
