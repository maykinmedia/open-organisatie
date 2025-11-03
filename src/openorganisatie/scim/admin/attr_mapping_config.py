from django.contrib import admin

from ..models.attr_mapping_config import AttribuutMappingConfig


@admin.register(AttribuutMappingConfig)
class AttribuutMappingConfigAdmin(admin.ModelAdmin):
    list_display = ("naam", "medewerker_koppel_attribuut")
    search_fields = ("naam", "medewerker_koppel_attribuut")
