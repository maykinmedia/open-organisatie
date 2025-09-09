import django_filters

from openorganisatie.scim.models.team import Team


class TeamFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    actief = django_filters.BooleanFilter(field_name="active", label="Actief")

    class Meta:
        model = Team
        fields = []
