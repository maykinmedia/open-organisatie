from reversion_compare.admin import CompareVersionAdmin


class ReadOnlyCompareVersionAdmin(CompareVersionAdmin):
    def has_change_permission(self, request, obj=None):
        return request.resolver_match.func.__name__ != "revision_view"
