from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.functie import Functie
from ..models.relaties import FunctieTeam, OrganisatorischeEenheidFunctie


class TeamFunctieInline(admin.StackedInline):
    model = FunctieTeam
    extra = 1


class OrganisatorischeEenheidFunctieInline(admin.StackedInline):
    model = OrganisatorischeEenheidFunctie
    extra = 1


@admin.register(Functie)
class FunctieAdmin(ReadOnlyCompareVersionAdmin):
    inlines = (
        TeamFunctieInline,
        OrganisatorischeEenheidFunctieInline,
    )
    list_display = (
        "external_id",
        "functie_omschrijving",
        "functie_type",
        "startdatum",
        "einddatum",
        "medewerker",
    )
    list_filter = ("functie_type", "startdatum", "einddatum")
    search_fields = ("functie_omschrijving", "functie_type__naam", "external_id")
    ordering = ("-startdatum",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "external_id",
                    "functie_omschrijving",
                    "functie_type",
                    "medewerker",
                )
            },
        ),
        (
            "Periode",
            {
                "fields": (
                    "startdatum",
                    "einddatum",
                    "wijzigingsdatum",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("functie_type")
