import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonFilter(django_filters.FilterSet):
    medewerker_uuid = django_filters.UUIDFilter(
        field_name="medewerker__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Contactpersoon", "medewerker"),
    )
    team_uuid = django_filters.UUIDFilter(
        field_name="teams__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Contactpersoon", "teams"),
    )
    organisatorischeEenheid_uuid = django_filters.UUIDFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Contactpersoon", "organisatorische_eenheden"),
    )

    class Meta:
        model = Contactpersoon
        fields = []
