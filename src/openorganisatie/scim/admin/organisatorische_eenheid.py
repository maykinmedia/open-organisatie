from django.contrib import admin

from ..models.organisatorische_eenheid import OrganisatorischeEenheid


@admin.register(OrganisatorischeEenheid)
class OrganisatorischeEenheidAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)
