from django.utils.translation import gettext_lazy as _

import django_filters
from vng_api_common.utils import get_help_text

from openorganisatie.identiteit.models.user import User
from openorganisatie.utils.filters import (
    UUIDFInFilter,
)


class UserFilter(django_filters.FilterSet):
    functie = django_filters.CharFilter(
        field_name="job_title",
        lookup_expr="icontains",
        label="Functie",
        help_text=get_help_text("identiteit.User", "job_title"),
    )
    actief = django_filters.BooleanFilter(
        field_name="is_active",
        label="Actief",
        help_text=get_help_text("identiteit.User", "is_active"),
    )
    groups_uuid = UUIDFInFilter(
        field_name="groups__scim_external_id",
        lookup_expr="in",
        distinct=True,
        help_text=_(
            "scim_external_id's van de gekoppelde groepen (via SCIM external ID)."
        ),
    )
    datum_toegevoegd = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="exact",
        help_text=get_help_text("identiteit.User", "date_joined"),
    )
    datum_toegevoegd__gt = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="gt",
        help_text=get_help_text("identiteit.User", "date_joined"),
    )
    datum_toegevoegd__lt = django_filters.IsoDateTimeFilter(
        field_name="date_joined",
        lookup_expr="lt",
        help_text=get_help_text("identiteit.User", "date_joined"),
    )

    class Meta:
        model = User
        fields = []
