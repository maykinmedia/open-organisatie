import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.enums.enums import GenderIndicator
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class MedewerkerFilter(django_filters.FilterSet):
    geslachtsaanduiding = django_filters.ChoiceFilter(
        field_name="gender_indicator",
        choices=GenderIndicator.choices,
        help_text=get_help_text("scim.Medewerker", "gender_indicator"),
    )
    teams_uuid = UUIDFInFilter(
        field_name="teams__uuid",
        lookup_expr="in",
        help_text=get_help_text("scim.Medewerker", "teams"),
    )
    organisatorische_eenheden_uuid = UUIDFInFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.Medewerker", "organisatorische_eenheden"),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.Medewerker", "functies"),
    )

    class Meta:
        model = Medewerker
        fields = []
