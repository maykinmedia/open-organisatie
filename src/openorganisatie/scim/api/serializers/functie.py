from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.functietype import FunctieType
from openorganisatie.utils.fields import UUIDRelatedField

from .functietype import FunctieTypeSerializer


class NestedFunctieSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.Functie", "uuid"),
    )
    functie_omschrijving = serializers.CharField(
        help_text=get_help_text("scim.Functie", "functie_omschrijving"),
    )
    begin_datum = serializers.DateField(
        help_text=get_help_text("scim.Functie", "begin_datum"),
    )
    eind_datum = serializers.DateField(
        allow_null=True,
        required=False,
        help_text=get_help_text("scim.Functie", "eind_datum"),
    )

    class Meta:
        model = Functie
        fields = [
            "uuid",
            "functie_omschrijving",
            "begin_datum",
            "eind_datum",
        ]


class FunctieSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.Functie", "uuid"),
    )
    functie_omschrijving = serializers.CharField(
        help_text=get_help_text("scim.Functie", "functie_omschrijving"),
    )
    begin_datum = serializers.DateField(
        help_text=get_help_text("scim.Functie", "begin_datum"),
    )
    eind_datum = serializers.DateField(
        allow_null=True,
        required=False,
        help_text=get_help_text("scim.Functie", "eind_datum"),
    )
    functie_type = FunctieTypeSerializer(
        required=False,
        read_only=True,
        help_text=get_help_text("scim.Functie", "functie_type"),
    )
    functietype_uuids = UUIDRelatedField(
        queryset=FunctieType.objects.all(),
        write_only=True,
        source="teams",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde teams."),
    )

    class Meta:
        model = Functie
        fields = [
            "uuid",
            "functie_omschrijving",
            "begin_datum",
            "eind_datum",
            "functie_type",
            "functietype_uuids",
        ]
