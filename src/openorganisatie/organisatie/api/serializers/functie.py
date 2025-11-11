from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import FunctieType
from openorganisatie.utils.fields import UUIDRelatedField

from .functietype import FunctieTypeSerializer


class NestedFunctieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Functie
        fields = [
            "uuid",
            "functie_omschrijving",
            "begin_datum",
            "eind_datum",
        ]


class FunctieSerializer(serializers.ModelSerializer):
    functie_type = FunctieTypeSerializer(
        required=False,
        read_only=True,
        help_text=get_help_text("organisatie.Functie", "functie_type"),
    )
    functietype_uuid = UUIDRelatedField(
        queryset=FunctieType.objects.all(),
        write_only=True,
        source="functie_type",
        help_text=_("UUID van de gekoppelde medewerker."),
    )

    class Meta:
        model = Functie
        fields = [
            "uuid",
            "functie_omschrijving",
            "begin_datum",
            "eind_datum",
            "functie_type",
            "functietype_uuid",
        ]
