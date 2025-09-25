import django_filters

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingFilter(django_filters.FilterSet):
    vestigingsnummer = django_filters.CharFilter(
        field_name="branchnumber", lookup_expr="icontains", label="Vestigingsnummer"
    )
    naam = django_filters.CharFilter(
        field_name="branchname", lookup_expr="icontains", label="Naam"
    )
    korte_naam = django_filters.CharFilter(
        field_name="short_name", lookup_expr="icontains", label="Korte naam"
    )
    adres = django_filters.CharFilter(
        field_name="address", lookup_expr="icontains", label="Adres"
    )
    correspondentieadres = django_filters.CharFilter(
        field_name="correspondence_address",
        lookup_expr="icontains",
        label="Correspondentieadres",
    )
    postadres = django_filters.CharFilter(
        field_name="postal_address", lookup_expr="icontains", label="Postadres"
    )
    telefoonnummer = django_filters.CharFilter(
        field_name="phone_number", lookup_expr="icontains", label="Telefoonnummer"
    )
    landcode = django_filters.CharFilter(
        field_name="country_code", lookup_expr="iexact", label="Landcode"
    )

    class Meta:
        model = Vestiging
        fields = []
