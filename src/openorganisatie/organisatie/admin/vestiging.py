from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(ReadOnlyCompareVersionAdmin):
    list_display = ("naam", "vestigingsnummer")
    search_fields = ("naam", "vestigingsnummer")
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
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
