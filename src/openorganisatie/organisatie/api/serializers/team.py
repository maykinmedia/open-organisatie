from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.team import Team
from openorganisatie.organisatie.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from .functie import NestedFunctieSerializer
from .organisatorische_eenheid import NestedMedewerkerSerializer
from .vestiging import VestigingSerializer


class NestedTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["uuid", "naam", "omschrijving"]


class TeamSerializer(serializers.ModelSerializer):
    contactpersoon = NestedMedewerkerSerializer(
        read_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "vestigingen"),
    )
    vestigingen = VestigingSerializer(
        many=True,
        read_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "vestigingen"),
    )
    vestigingen_uuid = UUIDRelatedField(
        queryset=Vestiging.objects.all(),
        write_only=True,
        many=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "vestigingen"),
        source="vestigingen",
    )
    functies = NestedFunctieSerializer(
        many=True,
        required=False,
        read_only=True,
        help_text=get_help_text("organisatie.Team", "functies"),
    )
    functies_uuid = UUIDRelatedField(
        queryset=Functie.objects.all(),
        write_only=True,
        source="functies",
        many=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "functies"),
    )

    class Meta:
        model = Team
        fields = [
            "uuid",
            "naam",
            "omschrijving",
            "contactpersoon",
            "vestigingen",
            "vestigingen_uuid",
            "functies",
            "functies_uuid",
        ]
