from django.contrib import admin

from ..models import Contactpersoon


@admin.register(Contactpersoon)
class ContactpersoonAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "medewerker",
        "get_team",
        "get_organisatorische_eenheid",
    )
    list_filter = (
        "team",
        "organisatorische_eenheid",
    )
    search_fields = (
        "medewerker__first_name",
        "medewerker__last_name",
        "team__name",
        "organisatorische_eenheid__name",
    )
    readonly_fields = ("uuid",)

    def get_team(self, obj):
        return obj.team.name if obj.team else "-"

    get_team.short_description = "Team"

    def get_organisatorische_eenheid(self, obj):
        return (
            obj.organisatorische_eenheid.name if obj.organisatorische_eenheid else "-"
        )

    get_organisatorische_eenheid.short_description = "Organisatorische Eenheid"
