from datetime import date

from django.test import TestCase

from psycopg.types.range import DateRange

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.team import TeamFactory

from ...admin.forms import FunctieTeamInlineForm


class FunctieTeamInlineFormTests(TestCase):
    def test_form_valid(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = FunctieTeamInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "periode_0": "2025-01-01",
                "periode_1": "2025-12-31",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

        periode = form.cleaned_data["periode"]

        self.assertEqual(periode.lower, date(2025, 1, 1))
        self.assertEqual(periode.upper, date(2025, 12, 31))

    def test_form_without_periode(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = FunctieTeamInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "periode_0": "",
                "periode_1": "",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertFalse(form.is_valid())
        self.assertIn("periode", form.errors)

    def test_form_invalid_startdatum(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = FunctieTeamInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "periode_0": "invalid-date",
                "periode_1": "2025-12-31",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("periode", form.errors)

    def test_form_invalid_einddatum(self):
        functie = FunctieFactory()
        team = TeamFactory()

        form = FunctieTeamInlineForm(
            data={
                "functie": functie.pk,
                "team": team.pk,
                "periode_0": "2025-01-01",
                "periode_1": "invalid-date",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("periode", form.errors)

    def test_widget_decompress(self):
        widget = FunctieTeamInlineForm.base_fields["periode"].widget

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
        widget = FunctieTeamInlineForm.base_fields["periode"].widget

        decompressed = widget.decompress(None)

        self.assertEqual(decompressed, [None, None])

    def test_widget_contains_placeholders(self):
        form = FunctieTeamInlineForm()

        html = str(form["periode"])

        self.assertIn("Startdatum", html)
        self.assertIn("Einddatum", html)

    def test_widget_uses_admin_date_widget(self):
        form = FunctieTeamInlineForm()

        html = str(form["periode"])

        self.assertIn("vDateField", html)
