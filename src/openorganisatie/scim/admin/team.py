from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    filter_horizontal = ("members",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("members")
