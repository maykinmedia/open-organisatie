from django.contrib import admin

from ..models.functie import Functie


@admin.register(Functie)
class FunctieAdmin(admin.ModelAdmin):
    list_display = (
        "functie_omschrijving",
        "functie_type",
        "begin_datum",
        "eind_datum",
    )
    list_filter = ("functie_type", "begin_datum", "eind_datum")
    search_fields = ("functie_omschrijving", "functie_type__naam")
    ordering = ("-begin_datum",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "functie_omschrijving",
                    "functie_type",
                )
            },
        ),
        (
            "Periode",
            {
                "fields": (
                    "begin_datum",
                    "eind_datum",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("functie_type")
