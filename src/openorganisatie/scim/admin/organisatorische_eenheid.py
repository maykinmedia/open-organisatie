from django.contrib import admin

from ..models.organisatorische_eenheid import OrganisatorischeEenheid


@admin.register(OrganisatorischeEenheid)
class OrganisatorischeEenheidAdmin(admin.ModelAdmin):
    list_display = ("name", "organization_type", "short_name")
    search_fields = ("name", "description", "short_name", "organization_type")
    list_filter = ("organization_type",)
    readonly_fields = ("uuid",)

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
                )
            },
        ),
        (
            "Contactgegevens",
            {"fields": ("email_address", "phone_number")},
        ),
        ("Status", {"fields": ("end_date",)}),
    )
