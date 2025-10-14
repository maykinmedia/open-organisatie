from django.contrib import admin

from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ("naam", "vestigingsnummer")
    search_fields = ("naam", "address")
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "vestigingsnummer",
                    "naam",
                    "verkorte_naam",
                    "landcode",
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
