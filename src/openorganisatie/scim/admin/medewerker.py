from django.contrib import admin

from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "job_title",
        "phone_number",
        "is_active",
        "date_joined",
        "last_modified",
        "display_teams",
    )
    readonly_fields = ("username", "date_joined", "last_modified", "display_teams")
    search_fields = ("first_name", "last_name", "email", "job_title")
    list_filter = ("is_active",)

    def display_teams(self, obj):
        return ", ".join([team.name for team in obj.scim_groups.all()])

    display_teams.short_description = "Teams"
