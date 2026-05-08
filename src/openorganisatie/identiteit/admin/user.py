from django.contrib import admin

from ...utils.reversion import ReadOnlyCompareVersionAdmin
from ..models.relaties import UserGroup
from ..models.user import User


class UserGroupInline(admin.StackedInline):
    model = UserGroup
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        from openorganisatie.identiteit.admin.forms import UserGroupInlineForm

        kwargs["form"] = UserGroupInlineForm
        return super().get_formset(request, obj, **kwargs)


@admin.register(User)
class UserAdmin(ReadOnlyCompareVersionAdmin):
    inlines = (UserGroupInline,)
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
            {"fields": ("medewerker",)},
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
