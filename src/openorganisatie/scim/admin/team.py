from django.contrib import admin

from ..models.team import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("naam", "actief")
    search_fields = ("naam", "beschrijving")
    list_filter = ("actief",)
    filter_horizontal = ("leden",)
