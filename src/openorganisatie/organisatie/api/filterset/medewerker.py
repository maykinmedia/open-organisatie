import django_filters

from openorganisatie.organisatie.models.medewerker import Medewerker


class MedewerkerFilter(django_filters.FilterSet):
    class Meta:
        model = Medewerker
        fields = {
            "external_id": ["exact"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "wijzigingsdatum": ["exact", "gte", "lte"],
        }
