import django_filters

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    functie = django_filters.CharFilter(
        field_name="function", lookup_expr="icontains", label="Functie"
    )

    class Meta:
        model = Contactpersoon
        fields = []
