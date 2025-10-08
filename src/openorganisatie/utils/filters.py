import django_filters


class UUIDFInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    pass
