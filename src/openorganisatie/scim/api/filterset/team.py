from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.team import Team
from openorganisatie.utils.filters import UUIDFInFilter


class TeamFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label=_("Naam"),
        help_text=get_help_text("scim.Team", "name"),
    )
    vestigingen_uuid = UUIDFInFilter(
        field_name="branches__uuid",
        lookup_expr="in",
        distinct=True,
        label=_("Vestigingen"),
        help_text=get_help_text("scim.Team", "branches"),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        label=_("Functies"),
        help_text=get_help_text("scim.Team", "functies"),
    )

    class Meta:
        model = Team
        fields = []
