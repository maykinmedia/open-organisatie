import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingFilter(django_filters.FilterSet):
    vestigingsnummer = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "vestigingsnummer"),
    )
    naam = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "naam"),
    )
    verkorte_naam = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "verkorte_naam"),
    )
    adres = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "adres"),
    )
    post_adres = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=get_help_text("scim.Vestiging", "post_adres"),
    )
    landcode = django_filters.CharFilter(
        lookup_expr="iexact",
        help_text=get_help_text("scim.Vestiging", "landcode"),
    )

    class Meta:
        model = Vestiging
        fields = []
