from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.team import Team


class TeamFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label=_("Naam"),
        help_text=get_help_text("scim.Team", "name"),
    )

    class Meta:
        model = Team
        fields = []
