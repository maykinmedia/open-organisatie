from django.contrib import admin

from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = (
        "voornaam",
        "achternaam",
        "emailadres",
        "functie",
        "telefoonnummer",
        "actief",
        "datum_toegevoegd",
        "laatst_gewijzigd",
    )
    readonly_fields = ("azure_oid", "datum_toegevoegd", "laatst_gewijzigd")
    search_fields = ("voornaam", "achternaam", "emailadres", "functie")
    list_filter = ("actief",)
