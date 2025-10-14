from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from .organisatorische_eenheid import NestedOrganisatorischeEenheidSerializer
from .team import NestedTeamSerializer


class NestedMedewerkerSerializer(serializers.ModelSerializer):
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
            "datum_aangepast",
        ]


class ContactpersoonSerializer(serializers.ModelSerializer):
    medewerker = NestedMedewerkerSerializer(
        read_only=True, help_text=get_help_text("scim.Contactpersoon", "medewerker")
    )
    teams = NestedTeamSerializer(
        read_only=True,
        many=True,
        help_text=get_help_text("scim.Contactpersoon", "teams"),
    )
    organisatorische_eenheden = NestedOrganisatorischeEenheidSerializer(
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
    teams_uuid = UUIDRelatedField(
        queryset=Team.objects.all(),
        write_only=True,
        source="teams",
        allow_null=True,
        required=False,
        many=True,
        help_text=_("UUID's van de gekoppelde teams."),
    )
    organisatorische_eenheden_uuid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
        source="organisatorische_eenheden",
        allow_null=True,
        required=False,
        many=True,
        help_text=_("UUID's van de gekoppelde organisatorsiche eenheden."),
    )

    class Meta:
        model = Contactpersoon
        fields = [
            "uuid",
            "medewerker",
            "medewerker_uuid",
            "teams",
            "teams_uuid",
            "organisatorische_eenheden",
            "organisatorische_eenheden_uuid",
        ]
