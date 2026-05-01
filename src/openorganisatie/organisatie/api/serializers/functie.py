from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from psycopg.types.range import DateRange
from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import FunctieType
from openorganisatie.organisatie.models.medewerker import Medewerker
from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)
from openorganisatie.organisatie.models.relaties import (
    FunctieTeam,
    OrganisatorischeEenheidFunctie,
)
from openorganisatie.organisatie.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from ..validators import (
    validate_functie_oe,
    validate_functie_team,
)
from .functietype import FunctieTypeSerializer
from .medewerker import MedewerkerSerializer
from .organisatorische_eenheid import NestedOrganisatorischeEenheidSerializer
from .team import NestedTeamSerializer


class PeriodSerializer(serializers.Serializer):
    startdatum = serializers.DateField()
    einddatum = serializers.DateField(required=False, allow_null=True)

    def to_representation(self, instance):
        return {
            "startdatum": instance.lower,
            "einddatum": instance.upper,
        }


class TeamGroupPeriodsSerializer(serializers.Serializer):
    team = NestedTeamSerializer()
    periodes = PeriodSerializer(many=True)
    wijzigingsdatum = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team",
            "periode",
            "wijzigingsdatum",
        ]


class OrganisatorischeEenheidGroupPeriodsSerializer(serializers.Serializer):
    organisatorische_eenheid = NestedOrganisatorischeEenheidSerializer()
    periodes = PeriodSerializer(many=True)
    wijzigingsdatum = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "team",
            "periode",
            "wijzigingsdatum",
        ]


class FunctieTeamSerializer(serializers.ModelSerializer):
    team = NestedTeamSerializer(read_only=True)
    periode = PeriodSerializer(read_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team",
            "periode",
            "wijzigingsdatum",
        ]


class FunctieTeamWriteSerializer(serializers.ModelSerializer):
    team_uuid = UUIDRelatedField(
        source="team",
        queryset=Team.objects.all(),
        write_only=True,
    )
    periode = PeriodSerializer(write_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team_uuid",
            "periode",
        ]


class OrganisatorischeEenheidFunctieSerializer(serializers.ModelSerializer):
    organisatorische_eenheid = NestedOrganisatorischeEenheidSerializer(read_only=True)
    periode = PeriodSerializer(read_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid",
            "periode",
            "wijzigingsdatum",
        ]


class OrganisatorischeEenheidFunctieWriteSerializer(serializers.ModelSerializer):
    organisatorische_eenheid_uuid = UUIDRelatedField(
        source="organisatorische_eenheid",
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
    )
    periode = PeriodSerializer(write_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid_uuid",
            "periode",
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
        help_text=_("UUID van de gekoppelde functietype."),
    )
    medewerker = MedewerkerSerializer(
        read_only=True,
    )
    medewerker_uuid = UUIDRelatedField(
        queryset=Medewerker.objects.all(),
        write_only=True,
        required=False,
        help_text=_("UUID van de gekoppelde medewerker."),
        source="medewerker",
    )
    teams = serializers.SerializerMethodField()
    teams_input = FunctieTeamWriteSerializer(
        many=True,
        write_only=True,
        required=False,
    )
    organisatorische_eenheden = serializers.SerializerMethodField()
    organisatorische_eenheden_input = OrganisatorischeEenheidFunctieWriteSerializer(
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
            "medewerker_uuid",
            "teams",
            "teams_input",
            "organisatorische_eenheden",
            "organisatorische_eenheden_input",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        validate_functie_team(self, attrs)
        validate_functie_oe(self, attrs)

        return attrs

    @extend_schema_field(TeamGroupPeriodsSerializer(many=True))
    def get_teams(self, obj):
        qs = obj.functieteam_set.select_related("team")

        grouped = {}

        for rel in qs:
            team_id = rel.team_id

            if team_id not in grouped:
                grouped[team_id] = {
                    "team": rel.team,
                    "periodes": [],
                    "wijzigingsdatum": rel.wijzigingsdatum,
                }

            grouped[team_id]["periodes"].append(rel.periode)

        return TeamGroupPeriodsSerializer(grouped.values(), many=True).data

    @extend_schema_field(OrganisatorischeEenheidGroupPeriodsSerializer(many=True))
    def get_organisatorische_eenheden(self, obj):
        qs = obj.organisatorischeeenheidfunctie_set.select_related(
            "organisatorische_eenheid"
        )

        grouped = {}

        for rel in qs:
            organisatorische_eenheid_id = rel.organisatorische_eenheid_id

            if organisatorische_eenheid_id not in grouped:
                grouped[organisatorische_eenheid_id] = {
                    "organisatorische_eenheid": rel.organisatorische_eenheid,
                    "periodes": [],
                    "wijzigingsdatum": rel.wijzigingsdatum,
                }

            grouped[organisatorische_eenheid_id]["periodes"].append(rel.periode)

        return OrganisatorischeEenheidGroupPeriodsSerializer(
            grouped.values(), many=True
        ).data

    def create(self, validated_data):
        teams_data = validated_data.pop("teams_input", [])
        oe_data = validated_data.pop("organisatorische_eenheden_input", [])

        with transaction.atomic():
            functie = super().create(validated_data)

            for team in teams_data:
                period_data = team.pop("periode")
                start = period_data["startdatum"]
                end = period_data.get("einddatum")

                FunctieTeam.objects.create(
                    functie=functie,
                    periode=DateRange(start, end),
                    **team,
                )

            for oe in oe_data:
                period_data = oe.pop("periode")
                start = period_data["startdatum"]
                end = period_data.get("einddatum")

                OrganisatorischeEenheidFunctie.objects.create(
                    functie=functie,
                    periode=DateRange(start, end),
                    **oe,
                )

        return functie

    # def update(self, instance, validated_data):
    #     teams_data = validated_data.pop("teams_input", None)
    #     oe_data = validated_data.pop("organisatorische_eenheden_input", None)

    #     return super().update(instance, validated_data)
