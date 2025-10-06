import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingFilter(django_filters.FilterSet):
    vestigingsnummer = django_filters.CharFilter(
        field_name="branchnumber",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "branchnumber"),
    )
    naam = django_filters.CharFilter(
        field_name="branchname",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "branchname"),
    )
    korte_naam = django_filters.CharFilter(
        field_name="short_name",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "short_name"),
    )
    adres = django_filters.CharFilter(
        field_name="address",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "address"),
    )
    postadres = django_filters.CharFilter(
        field_name="postal_address",
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "postal_address"),
    )
    landcode = django_filters.CharFilter(
        field_name="country_code",
        lookup_expr="iexact",
        help_text=get_help_text("scim.Vestiging", "country_code"),
    )

    class Meta:
        model = Vestiging
        fields = []
