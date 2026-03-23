from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.user import User


@admin.register(User)
class UserAdmin(ReadOnlyCompareVersionAdmin):
    list_display = (
        "employee_number",
        "email",
        "is_active",
        "date_joined",
        "last_modified",
    )
    readonly_fields = ("username", "scim_external_id", "date_joined", "last_modified")
    search_fields = ("email", "employee_number")
    list_filter = ("is_active",)
    filter_horizontal = ("groups",)

    fieldsets = (
        (
            "SCIM informatie",
            {"fields": ("scim_external_id",)},
        ),
        (
            "Algemene informatie",
            {
                "fields": (
                    "employee_number",
                    "username",
                    "email",
                )
            },
        ),
        (
            "Relaties",
            {"fields": ("groups", "medewerker")},
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "date_joined",
                    "last_modified",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("groups")
