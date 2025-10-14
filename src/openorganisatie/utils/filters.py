import django_filters
from django_filters.rest_framework import FilterSet as _FilterSet


class UUIDFInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    pass


class FilterSet(_FilterSet):
    """
    Add help texts for model field filters
    """

    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr=None):
        field_filter = super().filter_for_field(field, field_name, lookup_expr)

        if not field_filter.extra.get("help_text"):
            field_filter.extra["help_text"] = getattr(field, "help_text", None)
        return field_filter
