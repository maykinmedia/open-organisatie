from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.functie import Functie
from ..models.relaties import FunctieTeam, OrganisatorischeEenheidFunctie
from .forms import TemporalModelForm


class TeamFunctieInlineForm(TemporalModelForm):
    class Meta:
        model = FunctieTeam
        fields = ("geldigheid",)


class OrganisatorischeEenheidInlineForm(TemporalModelForm):
    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = ("geldigheid",)


class TeamFunctieInline(admin.StackedInline):
    form = TeamFunctieInlineForm
    model = FunctieTeam
    fields = (
        "team",
        "geldigheid",
    )

    extra = 1


class OrganisatorischeEenheidFunctieInline(admin.StackedInline):
    form = OrganisatorischeEenheidInlineForm
    model = OrganisatorischeEenheidFunctie
    fields = (
        "organisatorische_eenheid",
        "geldigheid",
    )
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
                    "vervanger",
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
