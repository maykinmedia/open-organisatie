from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.team import Team


@admin.register(Team)
class TeamAdmin(ReadOnlyCompareVersionAdmin):
    list_display = ("external_id", "naam", "contactpersoon")
    search_fields = (
        "naam",
        "omschrijving",
        "external_id",
    )
    readonly_fields = ("uuid",)
    filter_horizontal = ("vestigingen",)

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "external_id",
                    "naam",
                    "omschrijving",
                    "contactpersoon",
                    "soort_team",
                    "telefoonnummer",
                    "emailadres",
                    "startdatum",
                    "einddatum",
                    "wijzigingsdatum",
                )
            },
        ),
        (
            "Relaties",
            {"fields": ("vestigingen",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("vestigingen")
