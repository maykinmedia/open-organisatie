from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(ReadOnlyCompareVersionAdmin):
    list_display = (
        "external_id",
        "voornaam",
        "achternaam",
        "emailadres",
        "telefoonnummer",
        "startdatum",
        "einddatum",
    )
    readonly_fields = ("uuid", "startdatum", "einddatum")
    search_fields = ("voornaam", "achternaam", "emailadres", "external_id")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "external_id",
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
            "Status",
            {"fields": ("startdatum", "einddatum", "wijzigingsdatum")},
        ),
    )
