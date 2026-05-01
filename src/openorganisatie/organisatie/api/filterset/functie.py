from django.utils.translation import gettext_lazy as _

from django_filters import DateFilter

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
    team_uuid = UUIDFInFilter(
        field_name="functieteam__team__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde teams."),
    )
    organisatorische_eenheid_uuid = UUIDFInFilter(
        field_name="organisatorischeeenheidfunctie__organisatorische_eenheid__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde organisatorische eenheden."),
    )
    actief_op_team = DateFilter(
        field_name="functieteam__periode",
        lookup_expr="contains",
        distinct=True,
        help_text="Functies actief via team op deze datum",
    )
    actief_op_organisatorische_eenheid = DateFilter(
        field_name="organisatorischeeenheidfunctie__periode",
        lookup_expr="contains",
        distinct=True,
        help_text="Functies actief via organisatorische eenheid op deze datum",
    )

    class Meta:
        model = Functie
        fields = {
            "external_id": ["exact"],
            "functie_omschrijving": ["exact", "icontains"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "wijzigingsdatum": ["exact", "gte", "lte"],
        }
