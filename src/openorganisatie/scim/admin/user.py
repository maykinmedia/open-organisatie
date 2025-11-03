from django.contrib import admin

from ..models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
    readonly_fields = ("username", "scim_external_id", "date_joined", "last_modified")
    search_fields = ("first_name", "last_name", "email", "job_title")
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
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "job_title",
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
