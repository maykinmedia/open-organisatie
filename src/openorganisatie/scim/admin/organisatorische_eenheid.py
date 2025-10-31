from django.contrib import admin

from ..models.organisatorische_eenheid import OrganisatorischeEenheid


@admin.register(OrganisatorischeEenheid)
class OrganisatorischeEenheidAdmin(admin.ModelAdmin):
    list_display = ("naam", "soort_organisatie", "verkorte_naam", "contactpersoon")
    search_fields = ("naam", "omschrijving", "verkorte_naam", "soort_organisatie")
    list_filter = ("soort_organisatie",)
    readonly_fields = ("uuid",)
    filter_horizontal = ("vestigingen", "functies")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "uuid",
                    "identificatie",
                    "naam",
                    "verkorte_naam",
                    "soort_organisatie",
                    "omschrijving",
                    "datum_opheffing",
                    "contactpersoon",
                    "hoofd_organisatorische_eenheid",
                )
            },
        ),
        (
            "Contactgegevens",
            {"fields": ("emailadres", "telefoonnummer")},
        ),
        (
            "Relaties",
            {"fields": ("vestigingen", "functies")},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("vestigingen", "functies")
