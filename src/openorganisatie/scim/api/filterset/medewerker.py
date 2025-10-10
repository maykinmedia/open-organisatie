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
    )
    organisatorische_eenheden_uuid = UUIDFInFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="in",
        distinct=True,
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
    )

    class Meta:
        model = Medewerker
        fields = []
