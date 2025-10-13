from django.utils.translation import gettext_lazy as _

import django_filters

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.filters import FilterSet, UUIDFInFilter


class OrganisatorischeEenheidFilter(FilterSet):
    hoofd_organisatorische_eenheid = django_filters.UUIDFilter(
        lookup_expr="exact",
        help_text=_("UUID van de bovenliggende organisatorische eenheid."),
    )
    vestigingen_uuid = UUIDFInFilter(
        field_name="vestigingen__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde vestigingen."),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde functies."),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = {
            "naam": ["exact", "icontains"],
            "identificatie": ["exact"],
            "soort_organisatie": ["exact"],
            "verkorte_naam": ["exact"],
        }
