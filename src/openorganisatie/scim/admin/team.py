from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "display_medewerkers")
    search_fields = ("name", "description")
    readonly_fields = ("display_medewerkers", "uuid")
    filter_horizontal = ("branches", "functies")

    fieldsets = (
        ("Algemene informatie", {"fields": ("uuid", "name", "description")}),
        (
            "Medewerkers",
            {
                "fields": ("display_medewerkers",),
            },
        ),
        (
            "Relaties",
            {"fields": ("branches", "functies")},
        ),
    )

    def display_medewerkers(self, obj):
        return ", ".join(
            [
                f"{medewerker.first_name} {medewerker.last_name}"
                for medewerker in obj.medewerkers.all()
            ]
        )

    display_medewerkers.short_description = "Medewerkers"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("branches", "functies", "medewerkers")
        )
