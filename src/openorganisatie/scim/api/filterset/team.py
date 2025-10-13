from django.utils.translation import gettext_lazy as _

from openorganisatie.scim.models.team import Team
from openorganisatie.utils.filters import FilterSet, UUIDFInFilter


class TeamFilter(FilterSet):
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
        model = Team
        fields = {
            "naam": ["exact", "icontains"],
        }
