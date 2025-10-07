from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models import Medewerker
from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.functie import NestedFunctieSerializer
from ..serializers.organisatorische_eenheid import OrganisatorischeEenheidSerializer
from ..serializers.team import NestedTeamSerializer


class MedewerkerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "uuid"),
    )
    medewerker_id = serializers.CharField(
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "medewerker_id"),
    )
    voornaam = serializers.CharField(
        source="first_name",
        help_text=get_help_text("scim.Medewerker", "first_name"),
    )
    achternaam = serializers.CharField(
        source="last_name",
        help_text=get_help_text("scim.Medewerker", "last_name"),
    )
    emailadres = serializers.EmailField(
        source="email",
        help_text=get_help_text("scim.Medewerker", "email"),
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Medewerker", "phone_number"),
    )
    geslachtsaanduiding = serializers.ChoiceField(
        source="gender_indicator",
        choices=getattr(Medewerker._meta.get_field("gender_indicator"), "choices", []),
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Medewerker", "gender_indicator"),
    )
    datum_uit_dienst = serializers.DateField(
        source="termination_date",
        required=False,
        allow_null=True,
        help_text=get_help_text("scim.Medewerker", "termination_date"),
    )
    teams = NestedTeamSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "teams"),
    )
    team_uuids = UUIDRelatedField(
        queryset=Team.objects.all(),
        write_only=True,
        source="teams",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde teams."),
    )
    functies = NestedFunctieSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "functies"),
    )
    functie_uuids = UUIDRelatedField(
        queryset=Functie.objects.all(),
        write_only=True,
        source="functies",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde functies."),
    )
    organisatorische_eenheden = OrganisatorischeEenheidSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "organisatorische_eenheden"),
    )
    organisatorische_eenheid_uuids = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
        source="organisatorische_eenheden",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde organisatorische eenheden."),
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
            "team_uuids",
            "functies",
            "functie_uuids",
            "organisatorische_eenheden",
            "organisatorische_eenheid_uuids",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
