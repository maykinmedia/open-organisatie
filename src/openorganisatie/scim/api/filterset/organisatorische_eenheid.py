import django_filters

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    actief = django_filters.BooleanFilter(field_name="active", label="Actief")

    class Meta:
        model = OrganisatorischeEenheid
        fields = []
