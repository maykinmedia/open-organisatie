import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie


class FunctieFilter(django_filters.FilterSet):
    begin_datum = django_filters.DateFilter(
        field_name="begin_datum",
        help_text=get_help_text("scim.Functie", "begin_datum"),
    )
    eind_datum = django_filters.DateFilter(
        field_name="eind_datum",
        help_text=get_help_text("scim.Functie", "eind_datum"),
    )
    functie_type_uuid = django_filters.UUIDFilter(
        field_name="functie_type__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Functie", "functie_type"),
    )

    class Meta:
        model = Functie
        fields = []
