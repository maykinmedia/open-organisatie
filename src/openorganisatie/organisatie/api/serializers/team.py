from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.medewerker import Medewerker
from openorganisatie.organisatie.models.team import Team
from openorganisatie.organisatie.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from .organisatorische_eenheid import NestedMedewerkerSerializer
from .vestiging import VestigingSerializer


class NestedTeamSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[override]
        model = Team
        fields = [
            "uuid",
            "external_id",
            "naam",
            "omschrijving",
            "soort_team",
            "telefoonnummer",
            "emailadres",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
        ]


class TeamSerializer(serializers.ModelSerializer):
    contactpersoon = NestedMedewerkerSerializer(
        read_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "contactpersoon"),
    )
    contactpersoon_uuid = UUIDRelatedField(
        queryset=Medewerker.objects.all(),
        write_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "contactpersoon"),
        source="contactpersoon",
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

    class Meta:  # type: ignore[override]
        model = Team
        fields = [
            "uuid",
            "external_id",
            "naam",
            "omschrijving",
            "soort_team",
            "telefoonnummer",
            "emailadres",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
            "contactpersoon",
            "contactpersoon_uuid",
            "vestigingen",
            "vestigingen_uuid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
