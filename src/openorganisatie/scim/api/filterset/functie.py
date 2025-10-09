import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie


class FunctieFilter(django_filters.FilterSet):
    functie_omschrijving = django_filters.CharFilter(
        field_name="functie_omschrijving",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Functie", "functie_omschrijving"),
    )
    functie_type_uuid = django_filters.UUIDFilter(
        field_name="functie_type__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Functie", "functie_type"),
    )

    class Meta:
        model = Functie
        fields = []
