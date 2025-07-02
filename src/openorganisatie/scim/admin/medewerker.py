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
    )
    readonly_fields = ("azure_oid",)
    search_fields = ("voornaam", "achternaam", "emailadres", "functie")
    list_filter = ("actief",)
