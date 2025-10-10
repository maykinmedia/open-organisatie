from django.utils.translation import gettext_lazy as _

import django_filters

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class ContactpersoonFilter(django_filters.FilterSet):
    medewerker_uuid = django_filters.UUIDFilter(
        field_name="medewerker__uuid",
        lookup_expr="exact",
        distinct=True,
        help_text=_("UUID van de gekoppelde medewerker."),
    )
    teams_uuid = UUIDFInFilter(
        field_name="teams__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde teams."),
    )
    organisatorische_eenheden_uuid = UUIDFInFilter(
        field_name="organisatorische_eenheden__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde organisatorische eenheden."),
    )

    class Meta:
        model = Contactpersoon
        fields = []
