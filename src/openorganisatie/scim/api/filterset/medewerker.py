import django_filters

from openorganisatie.scim.models.medewerker import Medewerker


class MedewerkerFilter(django_filters.FilterSet):
    class Meta:
        model = Medewerker
        fields = [
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "termination_date",
        ]
