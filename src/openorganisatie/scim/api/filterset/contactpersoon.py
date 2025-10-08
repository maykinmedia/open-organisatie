import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class ContactpersoonFilter(django_filters.FilterSet):
    medewerker_uuid = django_filters.UUIDFilter(
        field_name="medewerker__uuid",
        lookup_expr="exact",
        distinct=True,
        help_text=get_help_text("scim.Contactpersoon", "medewerker"),
    )
    teams_uuid = UUIDFInFilter(
        field_name="teams__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.Contactpersoon", "teams"),
    )
    organisatorische_eenheden_uuid = UUIDFInFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.Contactpersoon", "organisatorische_eenheden"),
    )

    class Meta:
        model = Contactpersoon
        fields = []
