from django.contrib import admin

from ..models import Contactpersoon


@admin.register(Contactpersoon)
class ContactpersoonAdmin(admin.ModelAdmin):
    list_display = ("name", "function", "email_address", "phone_number", "uuid")
    search_fields = ("name", "email_address", "phone_number")
    list_filter = ("function",)
    readonly_fields = ("uuid",)

    fieldsets = (
        ("Algemene informatie", {"fields": ("uuid", "name", "function")}),
        ("Contactgegevens", {"fields": ("email_address", "phone_number")}),
    )
