from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("naam", "display_medewerkers", "contactpersoon")
    search_fields = ("naam", "omschrijving")
    readonly_fields = ("display_medewerkers", "uuid")
    filter_horizontal = ("vestigingen", "functies")

    fieldsets = (
        (
            "Algemene informatie",
            {"fields": ("uuid", "naam", "omschrijving", "contactpersoon")},
        ),
        (
            "Medewerkers",
            {
                "fields": ("display_medewerkers",),
            },
        ),
        (
            "Relaties",
            {"fields": ("vestigingen", "functies")},
        ),
    )

    def display_medewerkers(self, obj):
        return ", ".join(
            [
                f"{medewerker.voornaam} {medewerker.achternaam}"
                for medewerker in obj.medewerkers.all()
            ]
        )

    display_medewerkers.short_description = "Medewerkers"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("vestigingen", "functies", "medewerkers")
        )
