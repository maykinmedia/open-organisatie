from django.contrib.admin import ModelAdmin
from django.urls import path, re_path

from reversion_compare.admin import CompareVersionAdmin


class ReadOnlyCompareVersionAdmin(CompareVersionAdmin):
    def get_urls(self):
        """
        This way reversion VersionAdmin.get_urls is not called so that
        the recovery endpoints are not added.
        """
        urls = ModelAdmin.get_urls(self)
        admin_site = self.admin_site
        opts = self.model._meta
        reversion_urls = [
            re_path(
                r"^([^/]+)/history/(\d+)/$",
                admin_site.admin_view(self.revision_view),
                name=f"{opts.app_label}_{opts.model_name}_revision",
            ),
            path(
                "<str:object_id>/history/compare/",
                admin_site.admin_view(self.compare_view),
                name=f"{opts.app_label}_{opts.model_name}_compare",
            ),
        ]
        return reversion_urls + urls

    def has_change_permission(self, request, obj=None):
        return request.resolver_match.func.__name__ != "revision_view"
