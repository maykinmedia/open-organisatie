import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.group import Group
from openorganisatie.scim.models.user import User


class UserFilter(django_filters.FilterSet):
    functie = django_filters.CharFilter(
        field_name="job_title",
        lookup_expr="icontains",
        label="Functie",
        help_text=get_help_text("scim.User", "job_title"),
    )
    actief = django_filters.BooleanFilter(
        field_name="is_active",
        label="Actief",
        help_text=get_help_text("scim.User", "is_active"),
    )
    groups = django_filters.ModelMultipleChoiceFilter(
        field_name="groups__scim_external_id",
        queryset=Group.objects.all(),
        to_field_name="scim_external_id",
        label="Groups",
        help_text=get_help_text("scim.User", "groups"),
    )
    datum_toegevoegd = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="exact",
        help_text=get_help_text("scim.User", "date_joined"),
    )
    datum_toegevoegd__gt = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="gt",
        help_text=get_help_text("scim.User", "date_joined"),
    )
    datum_toegevoegd__lt = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="lt",
        help_text=get_help_text("scim.User", "date_joined"),
    )

    class Meta:
        model = User
        fields = []
