from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.forms import DateRangeField as FormDateRangeField

from ..models.relaties import UserGroup


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


class UserGroupInlineForm(forms.ModelForm):
    periode = FormDateRangeField(
        widget=DateRangeWidget(),
        label="Periode",
    )

    class Meta:
        model = UserGroup
        fields = (
            "user",
            "group",
            "periode",
        )
