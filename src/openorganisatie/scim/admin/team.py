from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)
    filter_horizontal = ("user_set",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("user_set")
