from django.contrib import admin

from ..models.medewerker import Medewerker


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "job_title",
        "phone_number",
        "is_active",
        "date_joined",
        "last_modified",
    )
    readonly_fields = ("username", "date_joined", "last_modified")
    search_fields = ("first_name", "last_name", "email", "job_title")
    list_filter = ("is_active",)
