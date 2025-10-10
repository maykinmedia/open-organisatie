import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class FunctieFilter(django_filters.FilterSet):
    functie_omschrijving = django_filters.CharFilter(
        field_name="functie_omschrijving",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Functie", "functie_omschrijving"),
    )
    functie_type_uuid = UUIDFInFilter(
        field_name="functie_type__uuid",
        lookup_expr="in",
        distinct=True,
    )

    class Meta:
        model = Functie
        fields = []
