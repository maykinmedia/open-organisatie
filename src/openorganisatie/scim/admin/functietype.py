from django.contrib import admin

from ..models.functietype import FunctieType


@admin.register(FunctieType)
class FunctieTypeAdmin(admin.ModelAdmin):
    list_display = ("uuid", "naam", "slug")
    search_fields = ("naam", "slug")
    prepopulated_fields = {"slug": ("naam",)}
    ordering = ("naam",)
    readonly_fields = ("uuid",)
