import django_filters

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonFilter(django_filters.FilterSet):
    functie = django_filters.CharFilter(field_name="function", lookup_expr="icontains")
    medewerker = django_filters.UUIDFilter(
        field_name="medewerker__uuid", lookup_expr="exact"
    )
    team = django_filters.UUIDFilter(field_name="team__uuid", lookup_expr="exact")

    class Meta:
        model = Contactpersoon
        fields = ["functie", "medewerker", "team"]
