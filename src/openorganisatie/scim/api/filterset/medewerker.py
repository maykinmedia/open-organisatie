from django.utils.translation import gettext_lazy as _

import django_filters

from openorganisatie.scim.enums.enums import GenderIndicator
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class MedewerkerFilter(django_filters.FilterSet):
    geslachtsaanduiding = django_filters.ChoiceFilter(
        choices=GenderIndicator.choices,
    )
    teams_uuid = UUIDFInFilter(
        field_name="teams__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde teams."),
    )
    organisatorische_eenheden_uuid = UUIDFInFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde organisatorische eenheden."),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde functies."),
    )

    class Meta:
        model = Medewerker
        fields = []
