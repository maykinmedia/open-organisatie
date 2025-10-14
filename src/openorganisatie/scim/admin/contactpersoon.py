from django.contrib import admin

from ..models import Contactpersoon


@admin.register(Contactpersoon)
class ContactpersoonAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "medewerker",
        "get_teams",
        "get_organisatorische_eenheden",
    )
    list_filter = (
        "teams",
        "organisatorische_eenheden",
    )
    search_fields = (
        "medewerker__voornaam",
        "medewerker__achternaam",
        "teams__naam",
        "organisatorische_eenheden__naam",
    )
    readonly_fields = ("uuid",)
    filter_horizontal = ("organisatorische_eenheden", "teams")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("medewerker")
            .prefetch_related("organisatorische_eenheden", "teams")
        )

    def get_teams(self, obj):
        return ", ".join([team.naam for team in obj.teams.all()]) or "-"

    get_teams.short_description = "Teams"

    def get_organisatorische_eenheden(self, obj):
        return ", ".join([oe.naam for oe in obj.organisatorische_eenheden.all()]) or "-"

    get_organisatorische_eenheden.short_description = "Organisatorische Eenheden"
