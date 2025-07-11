import django_filters

from openorganisatie.scim.models import Medewerker


class MedewerkerFilter(django_filters.FilterSet):
    functie = django_filters.CharFilter(
        field_name="job_title", lookup_expr="icontains", label="Functie"
    )
    geslachtsaanduiding = django_filters.BooleanFilter(
        field_name="gender_indicator", label="Geslachtsaanduiding"
    )
    datum_uit_dienst = django_filters.DateFilter(
        field_name="termination_date", label="Datum uit dienst"
    )
    actief = django_filters.BooleanFilter(field_name="is_active", label="Actief")
    datum_toegevoegd = django_filters.DateFilter(
        field_name="date_joined", label="Datum toegevoegd"
    )
    laatst_gewijzigd = django_filters.DateFilter(
        field_name="last_modified", label="Laatst gewijzigd"
    )

    class Meta:
        model = Medewerker
        fields = []
