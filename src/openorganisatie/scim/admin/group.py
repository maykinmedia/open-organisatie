from django.contrib import admin

from ..models.group import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "display_users")
    search_fields = ("name", "description")
    list_filter = ("active",)
    readonly_fields = ("display_users", "uuid")

    fieldsets = (
        ("Algemene informatie", {"fields": ("uuid", "name", "description", "active")}),
        (
            "Users",
            {
                "fields": ("display_users",),
            },
        ),
    )

    def display_users(self, obj):
        return ", ".join(
            [f"{user.first_name} {user.last_name}" for user in obj.user_set.all()]
        )

    display_users.short_description = "Users"
