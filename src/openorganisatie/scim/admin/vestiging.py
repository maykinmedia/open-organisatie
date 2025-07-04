from django.contrib import admin

from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ("naam", "organisatorische_eenheid", "actief")
    search_fields = ("naam", "adres")
    list_filter = ("actief", "organisatorische_eenheid")
    filter_horizontal = ("medewerkers",)
