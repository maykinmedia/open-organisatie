import django_filters

from openorganisatie.scim.models.group import Group
from openorganisatie.scim.models.user import User


class UserFilter(django_filters.FilterSet):
    functie = django_filters.CharFilter(
        field_name="job_title", lookup_expr="icontains", label="Functie"
    )
    datum_uit_dienst = django_filters.DateFilter(
        field_name="termination_date", label="Datum uit dienst"
    )
    actief = django_filters.BooleanFilter(field_name="is_active", label="Actief")
    groups = django_filters.ModelMultipleChoiceFilter(
        field_name="groups__scim_external_id",
        queryset=Group.objects.all(),
        to_field_name="scim_external_id",
        label="Groups",
    )
    datum_toegevoegd = django_filters.DateFilter(
        field_name="date_joined__date", label="Datum toegevoegd"
    )

    class Meta:
        model = User
        fields = []
