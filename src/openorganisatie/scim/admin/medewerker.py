from django.contrib import admin

from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = (
        "medewerker_id",
        "voornaam",
        "achternaam",
        "emailadres",
        "functie",
        "telefoonnummer",
        "actief",
    )
    search_fields = ("voornaam", "achternaam", "emailadres", "functie")
    list_filter = ("actief",)
