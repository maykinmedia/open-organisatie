from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.team import Team
from openorganisatie.scim.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from .functie import NestedFunctieSerializer
from .vestiging import VestigingSerializer


class NestedTeamSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.Team", "uuid"),
    )
    naam = serializers.CharField(
        source="name",
        help_text=get_help_text("scim.Team", "name"),
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        help_text=get_help_text("scim.Team", "description"),
    )

    class Meta:
        model = Team
        fields = ["uuid", "naam", "beschrijving"]


class TeamSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.Team", "uuid"),
    )
    naam = serializers.CharField(
        source="name",
        help_text=get_help_text("scim.Team", "name"),
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        help_text=get_help_text("scim.Team", "description"),
    )
    vestigingen = VestigingSerializer(
        many=True,
        read_only=True,
        required=False,
        help_text=get_help_text("scim.Team", "branches"),
    )
    vestiging_uuids = UUIDRelatedField(
        queryset=Vestiging.objects.all(),
        write_only=True,
        source="branches",
        many=True,
        required=False,
        help_text=get_help_text("scim.Team", "branches"),
    )
    functies = NestedFunctieSerializer(
        many=True,
        required=False,
        read_only=True,
        help_text=get_help_text("scim.Team", "functies"),
    )
    functie_uuids = UUIDRelatedField(
        queryset=Functie.objects.all(),
        write_only=True,
        source="functies",
        many=True,
        required=False,
        help_text=get_help_text("scim.Team", "functies"),
    )

    class Meta:
        model = Team
        fields = [
            "uuid",
            "naam",
            "beschrijving",
            "vestigingen",
            "vestiging_uuids",
            "functies",
            "functie_uuids",
        ]
