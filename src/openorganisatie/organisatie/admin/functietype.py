from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.functietype import FunctieType


@admin.register(FunctieType)
class FunctieTypeAdmin(ReadOnlyCompareVersionAdmin):
    list_display = ("external_id", "naam", "slug")
    search_fields = ("naam", "slug", "external_id")
    prepopulated_fields = {"slug": ("naam",)}
    ordering = ("naam",)
    readonly_fields = ("uuid",)
