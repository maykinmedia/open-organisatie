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
    filter_horizontal = ("scim_groups", "branch")

    fieldsets = (
        (
            "Algemene informatie",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "job_title",
                    "gender_indicator",
                )
            },
        ),
        (
            "Relaties",
            {
                "fields": (
                    "scim_groups",
                    "branch",
                    "contactpersoon",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "termination_date",
                    "date_joined",
                    "last_modified",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("scim_groups", "branch")
