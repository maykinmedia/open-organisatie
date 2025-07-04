from django.contrib import admin

from ..models.organisatorische_eenheid import OrganisatorischeEenheid


@admin.register(OrganisatorischeEenheid)
class OrganisatorischeEenheidAdmin(admin.ModelAdmin):
    list_display = ("naam", "actief")
    search_fields = ("naam", "beschrijving")
    list_filter = ("actief",)
