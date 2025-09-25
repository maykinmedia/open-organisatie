from django.contrib import admin

from ..models.organisatorische_eenheid import OrganisatorischeEenheid


@admin.register(OrganisatorischeEenheid)
class OrganisatorischeEenheidAdmin(admin.ModelAdmin):
    list_display = ("name", "organization_type", "short_name")
    search_fields = ("name", "description", "short_name", "organization_type")
    list_filter = ("organization_type",)
    readonly_fields = ("uuid",)
    filter_horizontal = ("branch", "functie")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "identifier",
                    "name",
                    "short_name",
                    "organization_type",
                    "description",
                    "end_date",
                )
            },
        ),
        (
            "Contactgegevens",
            {"fields": ("email_address", "phone_number")},
        ),
        (
            "Relaties",
            {"fields": ("branch", "functie")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("branch", "functie")
