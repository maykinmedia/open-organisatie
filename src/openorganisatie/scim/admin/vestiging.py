from django.contrib import admin

from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ("branchname", "branchnumber")
    search_fields = ("branchname", "address")
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "branchnumber",
                    "branchname",
                    "short_name",
                    "country_code",
                )
            },
        ),
        (
            "Contactgegevens",
            {
                "fields": (
                    "address",
                    "correspondence_address",
                    "postal_address",
                    "phone_number",
                )
            },
        ),
    )
