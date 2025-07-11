import django_filters

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    medewerkers = django_filters.ModelMultipleChoiceFilter(
        field_name="employees",
        queryset=Vestiging.objects.none(),  # Replace with Medewerker queryset if available
        label="Medewerkers",
    )
    organisatorische_eenheid = django_filters.ModelChoiceFilter(
        field_name="organisational_unit",
        queryset=Vestiging.objects.none(),  # Replace with OrganisatorischeEenheid queryset
        label="Organisatorische eenheid",
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
