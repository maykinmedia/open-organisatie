from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from .organisatorische_eenheid import OrganisatorischeEenheidSerializer
from .team import TeamSerializer


class NestedMedewerkerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Medewerker", "uuid")
    )
    medewerker_id = serializers.CharField(
        read_only=True, help_text=get_help_text("scim.Medewerker", "medewerker_id")
    )
    voornaam = serializers.CharField(
        source="first_name",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "first_name"),
    )
    achternaam = serializers.CharField(
        source="last_name",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "last_name"),
    )
    emailadres = serializers.EmailField(
        source="email",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "email"),
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "phone_number"),
    )
    geslachtsaanduiding = serializers.BooleanField(
        source="gender_indicator",
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "gender_indicator"),
    )
    datum_uit_dienst = serializers.DateField(
        source="termination_date",
        read_only=True,
        required=False,
        allow_null=True,
        help_text=get_help_text("scim.Medewerker", "termination_date"),
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
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]


class ContactpersoonSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Contactpersoon", "uuid")
    )

    medewerker = NestedMedewerkerSerializer(
        read_only=True, help_text=get_help_text("scim.Contactpersoon", "medewerker")
    )
    team = TeamSerializer(
        read_only=True,
        many=True,
        help_text=get_help_text("scim.Contactpersoon", "teams"),
    )
    organisatorischeEenheid = OrganisatorischeEenheidSerializer(
        read_only=True,
        many=True,
        help_text=get_help_text("scim.Contactpersoon", "organisatorische_eenheden"),
    )

    medewerker_uuid = UUIDRelatedField(
        queryset=Medewerker.objects.all(),
        write_only=True,
        source="medewerker",
        help_text=_("UUID van de gekoppelde medewerker."),
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
    organisatorischeEenheid_uuid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
        source="organisatorische_eenheid",
        allow_null=True,
        required=False,
        many=True,
        help_text=_("UUID van de gekoppelde organisatorsiche eenheden."),
    )

    class Meta:
        model = Contactpersoon
        fields = [
            "uuid",
            "medewerker",
            "medewerker_uuid",
            "team",
            "team_uuid",
            "organisatorischeEenheid",
            "organisatorischeEenheid_uuid",
        ]
