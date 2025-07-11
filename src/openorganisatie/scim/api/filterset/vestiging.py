import django_filters

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    actief = django_filters.BooleanFilter(field_name="active", label="Actief")
    datum_toegevoegd = django_filters.DateFilter(
        field_name="date_created", lookup_expr="gte", label="Datum toegevoegd"
    )
    laatst_gewijzigd = django_filters.DateFilter(
        field_name="last_modified", lookup_expr="gte", label="Laatst gewijzigd"
    )

    class Meta:
        model = Vestiging
        fields = []
