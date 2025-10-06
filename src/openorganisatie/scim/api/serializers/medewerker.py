from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models import Medewerker
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.team import TeamSerializer


class MedewerkerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Medewerker", "uuid")
    )
    medewerker_id = serializers.CharField(
        read_only=True, help_text=get_help_text("scim.Medewerker", "medewerker_id")
    )
    voornaam = serializers.CharField(
        source="first_name", help_text=get_help_text("scim.Medewerker", "first_name")
    )
    achternaam = serializers.CharField(
        source="last_name", help_text=get_help_text("scim.Medewerker", "last_name")
    )
    emailadres = serializers.EmailField(
        source="email", help_text=get_help_text("scim.Medewerker", "email")
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Medewerker", "phone_number"),
    )
    geslachtsaanduiding = serializers.BooleanField(
        source="gender_indicator",
        help_text=get_help_text("scim.Medewerker", "gender_indicator"),
    )
    datum_uit_dienst = serializers.DateField(
        source="termination_date",
        required=False,
        allow_null=True,
        help_text=get_help_text("scim.Medewerker", "termination_date"),
    )
    teams = TeamSerializer(
        many=True, read_only=True, help_text=get_help_text("scim.Medewerker", "teams")
    )
    team_uuid = UUIDRelatedField(
        queryset=Team.objects.all(),
        write_only=True,
        source="team",
        allow_null=True,
        required=False,
        many=True,
        help_text=_("UUID van de gekoppelde teams."),
    )
    datum_toegevoegd = serializers.DateTimeField(
        source="date_joined",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "date_joined"),
    )
    laatst_gewijzigd = serializers.DateTimeField(
        source="last_modified",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "last_modified"),
    )

    class Meta:
        model = Medewerker
        fields = [
            "uuid",
            "medewerker_id",
            "voornaam",
            "achternaam",
            "emailadres",
            "telefoonnummer",
            "geslachtsaanduiding",
            "datum_uit_dienst",
            "teams",
            "team_uuid",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
