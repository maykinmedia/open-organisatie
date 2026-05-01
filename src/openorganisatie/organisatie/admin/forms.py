from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.forms import DateRangeField as FormDateRangeField

from ..models.relaties import FunctieTeam


class DateRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            AdminDateWidget(
                attrs={
                    "placeholder": "Startdatum",
                }
            ),
            AdminDateWidget(
                attrs={
                    "placeholder": "Einddatum",
                }
            ),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.lower, value.upper]
        return [None, None]


class FunctieTeamInlineForm(forms.ModelForm):
    period = FormDateRangeField(
        widget=DateRangeWidget(),
        label="Periode",
    )

    class Meta:
        model = FunctieTeam
        fields = "__all__"

    def clean_period(self):
        value = self.cleaned_data.get("period")

        if not value:
            return None

        return value


class FunctieOrganisatorischeEenheidInlineForm(forms.ModelForm):
    period = FormDateRangeField(
        widget=DateRangeWidget(),
        label="Periode",
    )

    class Meta:
        model = FunctieTeam
        fields = "__all__"

    def clean_period(self):
        value = self.cleaned_data.get("period")

        if not value:
            return None

        return value
