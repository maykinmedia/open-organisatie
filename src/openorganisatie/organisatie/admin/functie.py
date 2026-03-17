from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.functie import Functie


@admin.register(Functie)
class FunctieAdmin(ReadOnlyCompareVersionAdmin):
    list_display = (
        "functie_omschrijving",
        "functie_type",
        "startdatum",
        "einddatum",
    )
    list_filter = ("functie_type", "startdatum", "einddatum")
    search_fields = ("functie_omschrijving", "functie_type__naam")
    ordering = ("-startdatum",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "functie_omschrijving",
                    "functie_type",
                )
            },
        ),
        (
            "Periode",
            {
                "fields": (
                    "startdatum",
                    "einddatum",
                    "wijzigingsdatum",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("functie_type")
