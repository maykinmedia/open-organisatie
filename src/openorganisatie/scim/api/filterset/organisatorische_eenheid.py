from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.filters import UUIDFInFilter


class OrganisatorischeEenheidFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "name"),
    )
    identificatie = django_filters.CharFilter(
        field_name="identifier",
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "identifier"),
    )
    type_organisatie = django_filters.CharFilter(
        field_name="organization_type",
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "organization_type"),
    )
    verkorte_naam = django_filters.CharFilter(
        field_name="short_name",
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "short_name"),
    )
    hoofd_organisatorische_eenheid = django_filters.UUIDFilter(
        field_name="parent_organisation__uuid",
        lookup_expr="exact",
        help_text=_("UUID van de bovenliggende organisatorische eenheid."),
    )
    vestigingen_uuid = UUIDFInFilter(
        field_name="branches__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "branches"),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "functies"),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = []
