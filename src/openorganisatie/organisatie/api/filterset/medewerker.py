from django.utils.translation import gettext_lazy as _

import django_filters

from openorganisatie.organisatie.models.medewerker import Medewerker
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class MedewerkerFilter(django_filters.FilterSet):
    teams_uuid = UUIDFInFilter(
        field_name="teams__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde teams."),
    )
    functies_uuid = UUIDFInFilter(
        field_name="functies__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde functies."),
    )

    class Meta:
        model = Medewerker
        fields = ("geslachtsaanduiding",)
