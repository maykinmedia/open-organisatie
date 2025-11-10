from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models import Medewerker
from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.functie import NestedFunctieSerializer
from ..serializers.team import NestedTeamSerializer


class MedewerkerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="scim_api:medewerker-detail", lookup_field="uuid"
    )
    teams = NestedTeamSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.Medewerker", "teams"),
    )
    teams_uuids = UUIDRelatedField(
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
    functies_uuids = UUIDRelatedField(
        queryset=Functie.objects.all(),
        write_only=True,
        source="functies",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde functies."),
    )

    class Meta:
        model = Medewerker
        fields = [
            "url",
            "uuid",
            "medewerker_id",
            "voornaam",
            "achternaam",
            "emailadres",
            "telefoonnummer",
            "geslachtsaanduiding",
            "datum_uit_dienst",
            "teams",
            "teams_uuids",
            "functies",
            "functies_uuids",
            "datum_toegevoegd",
            "datum_aangepast",
        ]
