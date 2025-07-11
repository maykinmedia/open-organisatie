from django.contrib import admin

from ..models.vestiging import Vestiging


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ("name", "organisational_unit", "active")
    search_fields = ("name", "address")
    list_filter = ("active", "organisational_unit")
    filter_horizontal = ("employees",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("organisational_unit")
            .prefetch_related("employees")
        )
