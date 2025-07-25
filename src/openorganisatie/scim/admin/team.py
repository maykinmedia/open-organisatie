from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "display_medewerkers")
    search_fields = ("name", "description")
    list_filter = ("active",)
    readonly_fields = ("display_medewerkers",)

    def display_medewerkers(self, obj):
        return ", ".join(
            [
                f"{medewerker.first_name} {medewerker.last_name}"
                for medewerker in obj.user_set.all()
            ]
        )

    display_medewerkers.short_description = "Medewerkers"
