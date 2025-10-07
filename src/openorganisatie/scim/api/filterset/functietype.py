import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functietype import FunctieType


class FunctieTypeFilter(django_filters.FilterSet):
    naam = django_filters.CharFilter(
        field_name="naam",
        lookup_expr="icontains",
        help_text=get_help_text("scim.FunctieType", "naam"),
    )
    slug = django_filters.CharFilter(
        field_name="slug",
        lookup_expr="exact",
        help_text=get_help_text("scim.FunctieType", "slug"),
    )

    class Meta:
        model = FunctieType
        fields = []
