from django.contrib import admin

from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = (
        "voornaam",
        "achternaam",
        "emailadres",
        "telefoonnummer",
        "datum_toegevoegd",
        "datum_aangepast",
    )
    readonly_fields = ("medewerker_id", "datum_toegevoegd", "datum_aangepast")
    search_fields = ("voornaam", "achternaam", "emailadres")
    filter_horizontal = ("teams", "functies", "organisatorische_eenheden")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
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
                    "organisatorische_eenheden",
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
        return (
            super()
            .get_queryset(request)
            .prefetch_related("teams", "organisatorische_eenheden", "functies")
        )
