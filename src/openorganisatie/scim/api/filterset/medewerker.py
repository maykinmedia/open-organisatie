import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.medewerker import Medewerker


class MedewerkerFilter(django_filters.FilterSet):
    geslachtsaanduiding = django_filters.BooleanFilter(
        field_name="gender_indicator",
        help_text=get_help_text("scim.Medewerker", "gender_indicator"),
    )
    datum_uit_dienst = django_filters.DateFilter(
        field_name="termination_date",
        help_text=get_help_text("scim.Medewerker", "termination_date"),
    )
    team_uuid = django_filters.UUIDFilter(
        field_name="teams__uuid",
        lookup_expr="exact",
        help_text=get_help_text("scim.Medewerker", "teams"),
    )
    datum_toegevoegd = django_filters.DateFromToRangeFilter(
        field_name="date_joined",
        help_text=get_help_text("scim.Medewerker", "date_joined"),
    )

    class Meta:
        model = Medewerker
        fields = []
