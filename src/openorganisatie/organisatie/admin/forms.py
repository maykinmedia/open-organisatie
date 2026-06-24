from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.forms import DateRangeField as FormDateRangeField
from django.utils.translation import gettext_lazy as _


class DateRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            AdminDateWidget(
                attrs={
                    "placeholder": _("Begin geldigheid"),
                }
            ),
            AdminDateWidget(
                attrs={
                    "placeholder": _("Einde geldigheid"),
                }
            ),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.lower, value.upper]
        return [None, None]


class TemporalModelForm(forms.ModelForm):
    geldigheid = FormDateRangeField(
        widget=DateRangeWidget(),
        required=True,
    )

    class Meta:
        abstract = True
