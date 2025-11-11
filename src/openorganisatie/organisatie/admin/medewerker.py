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
        "datum_toegevoegd",
        "datum_aangepast",
    )
    readonly_fields = ("uuid", "datum_toegevoegd", "datum_aangepast")
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
            {
                "fields": (
                    "datum_uit_dienst",
                    "datum_toegevoegd",
                    "datum_aangepast",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("teams", "functies")
