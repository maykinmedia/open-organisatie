from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFilter(django_filters.FilterSet):
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
    einddatum = django_filters.DateFilter(
        field_name="end_date",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "end_date"),
    )
    hoofd_organisatorische_eenheid = django_filters.UUIDFilter(
        field_name="parent_organisation__uuid",
        lookup_expr="exact",
        help_text=_("UUID van de bovenliggende organisatorische eenheid."),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = []
