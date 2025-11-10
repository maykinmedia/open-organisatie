import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.identiteit.models.group import Group


class GroupFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Naam",
        help_text=get_help_text("identiteit.Group", "name"),
    )
    actief = django_filters.BooleanFilter(
        field_name="active",
        label="Actief",
        help_text=get_help_text("identiteit.Group", "active"),
    )

    class Meta:
        model = Group
        fields = []
