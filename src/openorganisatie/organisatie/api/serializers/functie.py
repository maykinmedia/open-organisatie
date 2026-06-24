from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
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

from ..service import update_relations
from ..validators import (
    validate_functie_oe,
    validate_functie_team,
)
from .fields import PeriodField
from .functietype import FunctieTypeSerializer
from .medewerker import MedewerkerSerializer
from .organisatorische_eenheid import NestedOrganisatorischeEenheidSerializer
from .team import NestedTeamSerializer


class TeamGroupPeriodsSerializer(serializers.Serializer):
    team = NestedTeamSerializer()
    geldigheid = serializers.ListField(child=PeriodField())
    wijzigingsdatum = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team",
            "geldigheid",
            "wijzigingsdatum",
        ]


class OrganisatorischeEenheidGroupPeriodsSerializer(serializers.Serializer):
    organisatorische_eenheid = NestedOrganisatorischeEenheidSerializer()
    geldigheid = serializers.ListField(child=PeriodField())
    wijzigingsdatum = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid",
            "geldigheid",
            "wijzigingsdatum",
        ]


class FunctieTeamSerializer(serializers.ModelSerializer):
    team = NestedTeamSerializer(read_only=True)
    geldigheid = PeriodField(read_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team",
            "geldigheid",
        ]


class FunctieTeamWriteSerializer(serializers.ModelSerializer):
    team_uuid = UUIDRelatedField(
        source="team",
        queryset=Team.objects.all(),
        write_only=True,
    )
    geldigheid = PeriodField(write_only=True)

    class Meta:
        model = FunctieTeam
        fields = [
            "team_uuid",
            "geldigheid",
        ]


class OrganisatorischeEenheidFunctieSerializer(serializers.ModelSerializer):
    organisatorische_eenheid = NestedOrganisatorischeEenheidSerializer(read_only=True)
    geldigheid = PeriodField(read_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid",
            "geldigheid",
        ]


class OrganisatorischeEenheidFunctieWriteSerializer(serializers.ModelSerializer):
    organisatorische_eenheid_uuid = UUIDRelatedField(
        source="organisatorische_eenheid",
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
    )
    geldigheid = PeriodField(write_only=True)

    class Meta:
        model = OrganisatorischeEenheidFunctie
        fields = [
            "organisatorische_eenheid_uuid",
            "geldigheid",
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

        if self.instance is None:
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
                    "geldigheid": [],
                    "wijzigingsdatum": rel.wijzigingsdatum,
                }

            grouped[team_id]["geldigheid"].append(rel.geldigheid)

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
                    "geldigheid": [],
                    "wijzigingsdatum": rel.wijzigingsdatum,
                }

            grouped[organisatorische_eenheid_id]["geldigheid"].append(rel.geldigheid)

        return OrganisatorischeEenheidGroupPeriodsSerializer(
            grouped.values(), many=True
        ).data

    def _create_functieteam(self, instance, data):
        return FunctieTeam.objects.create(
            functie=instance,
            **data,
        )

    def _create_oe(self, instance, data):
        return OrganisatorischeEenheidFunctie.objects.create(
            functie=instance,
            **data,
        )

    def create(self, validated_data):
        teams_data = validated_data.pop("teams_input", [])
        oe_data = validated_data.pop("organisatorische_eenheden_input", [])

        try:
            with transaction.atomic():
                functie = super().create(validated_data)

                for team in teams_data:
                    self._create_functieteam(functie, team)

                for oe in oe_data:
                    self._create_oe(functie, oe)

            return functie
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

    def update(self, instance, validated_data):
        teams_data = validated_data.pop("teams_input", None)
        oe_data = validated_data.pop("organisatorische_eenheden_input", None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            update_relations(
                functie=instance,
                teams_data=teams_data,
                oe_data=oe_data,
            )

        return instance
