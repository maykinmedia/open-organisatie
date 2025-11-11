from django.utils.translation import gettext_lazy as _

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.utils.filters import (
    FilterSet,
    UUIDFInFilter,
)


class FunctieFilter(FilterSet):
    functie_type_uuid = UUIDFInFilter(
        field_name="functie_type__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde functietypen."),
    )

    class Meta:
        model = Functie
        fields = {
            "functie_omschrijving": ["exact", "icontains"],
        }
