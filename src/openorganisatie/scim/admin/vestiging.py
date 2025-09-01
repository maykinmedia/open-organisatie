from django.contrib import admin

from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ("branchname", "organisational_unit", "branchnumber")
    search_fields = ("branchname", "address")
    list_filter = ("organisational_unit",)
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
        (
            "Relaties",
            {"fields": ("organisational_unit",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("organisational_unit")
