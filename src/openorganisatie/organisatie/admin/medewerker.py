from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(ReadOnlyCompareVersionAdmin):
    list_display = (
        "voornaam",
        "achternaam",
        "emailadres",
        "telefoonnummer",
        "startdatum",
        "einddatum",
    )
    readonly_fields = ("uuid", "startdatum", "einddatum")
    search_fields = ("voornaam", "achternaam", "emailadres")
    filter_horizontal = ("teams", "functies")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "medewerker_id",
                    "voornaam",
                    "achternaam",
                    "emailadres",
                    "telefoonnummer",
                    "geslachtsaanduiding",
                )
            },
        ),
        (
            "Relaties",
            {
                "fields": (
                    "teams",
                    "functies",
                )
            },
        ),
        (
            "Status",
            {"fields": ("startdatum", "einddatum", "wijzigingsdatum")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("teams", "functies")
