import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.team import Team
from openorganisatie.utils.filters import UUIDFInFilter


class TeamFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Team", "naam"),
    )
    vestigingen_uuid = UUIDFInFilter(
        field_name="vestigingen__uuid",
        lookup_expr="in",
        distinct=True,
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
    )

    class Meta:
        model = Team
        fields = []
