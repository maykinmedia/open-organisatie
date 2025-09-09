import django_filters

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFilter(django_filters.FilterSet):
    identificatie = django_filters.CharFilter(
        field_name="identifier", lookup_expr="icontains", label="Identificatie"
    )
    naam = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Naam"
    )
    type_organisatie = django_filters.CharFilter(
        field_name="organization_type",
        lookup_expr="icontains",
        label="Type organisatie",
    )
    verkorte_naam = django_filters.CharFilter(
        field_name="short_name", lookup_expr="icontains", label="Verkorte naam"
    )
    beschrijving = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains", label="Beschrijving"
    )
    emailadres = django_filters.CharFilter(
        field_name="email_address", lookup_expr="icontains", label="E-mailadres"
    )
    telefoonnummer = django_filters.CharFilter(
        field_name="phone_number", lookup_expr="icontains", label="Telefoonnummer"
    )
    einddatum = django_filters.DateFilter(field_name="end_date", label="Einddatum")

    class Meta:
        model = OrganisatorischeEenheid
        fields = []
