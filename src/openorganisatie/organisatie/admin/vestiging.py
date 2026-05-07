from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(ReadOnlyCompareVersionAdmin):
    list_display = ("external_id", "naam", "vestigingsnummer")
    search_fields = (
        "naam",
        "vestigingsnummer",
        "external_id",
    )
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "external_id",
                    "vestigingsnummer",
                    "kvk_nummer",
                    "naam",
                )
            },
        ),
        (
            "Contactgegevens",
            {
                "fields": (
                    "adres",
                    "correspondentieadres",
                    "post_adres",
                    "telefoonnummer",
                )
            },
        ),
    )
