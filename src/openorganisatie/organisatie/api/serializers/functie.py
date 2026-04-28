from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import FunctieType
from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)
from openorganisatie.organisatie.models.relaties import (
    FunctieTeam,
    OrganisatorischeEenheidFunctie,
)
from openorganisatie.organisatie.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from .functietype import FunctieTypeSerializer
from .medewerker import MedewerkerSerializer
from .organisatorische_eenheid import NestedOrganisatorischeEenheidSerializer
from .team import NestedTeamSerializer


class FunctieTeamSerializer(serializers.ModelSerializer):
    team = NestedTeamSerializer(read_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
        ]


class FunctieTeamWriteSerializer(serializers.ModelSerializer):
    team_uuid = UUIDRelatedField(
        source="team",
        queryset=Team.objects.all(),
        write_only=True,
    )

    class Meta:
        model = FunctieTeam
        fields = [
            "team_uuid",
            "startdatum",
            "einddatum",
        ]


class OrganisatorischeEenheidFunctieSerializer(serializers.ModelSerializer):
    organisatorische_eenheid = NestedOrganisatorischeEenheidSerializer(read_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
        ]


class OrganisatorischeEenheidFunctieWriteSerializer(serializers.ModelSerializer):
    organisatorische_eenheid_uuid = UUIDRelatedField(
        source="organisatorische_eenheid",
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
    )

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid_uuid",
            "startdatum",
            "einddatum",
        ]


class NestedFunctieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Functie
        fields = [
            "uuid",
            "external_id",
            "functie_omschrijving",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
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
    medewerker = MedewerkerSerializer(
        many=True,
        read_only=True,
    )
    teams = FunctieTeamSerializer(
        source="functieteam_set",
        many=True,
        read_only=True,
    )
    teams_input = FunctieTeamWriteSerializer(
        source="functieteam_set",
        many=True,
        write_only=True,
        required=False,
    )
    organisatorische_eenheden = OrganisatorischeEenheidFunctieSerializer(
        source="organisatorischeeenheidfunctie_set",
        many=True,
        read_only=True,
    )
    organisatorische_eenheden_input = OrganisatorischeEenheidFunctieWriteSerializer(
        source="organisatorischeeenheidfunctie_set",
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Functie
        fields = [
            "uuid",
            "external_id",
            "functie_omschrijving",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
            "functie_type",
            "functietype_uuid",
            "medewerker",
            "teams",
            "teams_input",
            "organisatorische_eenheden",
            "organisatorische_eenheden_input",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
