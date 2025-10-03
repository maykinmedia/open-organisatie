import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.group import Group


class GroupFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Naam",
        help_text=get_help_text("scim.Group", "name"),
    )
    actief = django_filters.BooleanFilter(
        field_name="active",
        label="Actief",
        help_text=get_help_text("scim.Group", "active"),
    )

    class Meta:
        model = Group
        fields = []
