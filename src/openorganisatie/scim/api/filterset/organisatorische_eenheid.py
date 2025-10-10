from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.filters import UUIDFInFilter


class OrganisatorischeEenheidFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "naam"),
    )
    identificatie = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "identificatie"),
    )
    soort_organisatie = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "soort_organisatie"),
    )
    verkorte_naam = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "verkorte_naam"),
    )
    hoofd_organisatorische_eenheid = django_filters.UUIDFilter(
        lookup_expr="exact",
        help_text=_("UUID van de bovenliggende organisatorische eenheid."),
    )
    vestigingen_uuid = UUIDFInFilter(
        field_name="vestigingen__uuid",
        lookup_expr="in",
        distinct=True,
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = []
