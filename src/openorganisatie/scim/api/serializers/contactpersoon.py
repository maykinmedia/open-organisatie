from rest_framework import serializers

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.team import Team
from openorganisatie.utils.fields import UUIDRelatedField

from .organisatorische_eenheid import OrganisatorischeEenheidSerializer
from .team import TeamSerializer


class NestedMedewerkerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    medewerker_id = serializers.CharField(read_only=True)
    voornaam = serializers.CharField(source="first_name")
    achternaam = serializers.CharField(source="last_name")
    emailadres = serializers.EmailField(source="email")
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    geslachtsaanduiding = serializers.BooleanField(source="gender_indicator")
    datum_uit_dienst = serializers.DateField(
        source="termination_date", required=False, allow_null=True
    )
    datum_toegevoegd = serializers.DateTimeField(source="date_joined", read_only=True)
    laatst_gewijzigd = serializers.DateTimeField(source="last_modified", read_only=True)

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
    uuid = serializers.UUIDField()

    medewerker = NestedMedewerkerSerializer(read_only=True)
    team = TeamSerializer(read_only=True, many=True)
    organisatorischeEenheid = OrganisatorischeEenheidSerializer(
        read_only=True, many=True
    )

    medewerker_uuid = UUIDRelatedField(
        queryset=Medewerker.objects.all(),
        write_only=True,
        source="medewerker",
    )
    team_uuid = UUIDRelatedField(
        queryset=Team.objects.all(),
        write_only=True,
        source="team",
        allow_null=True,
        required=False,
    )
    organisatorischeEenheid_uuid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        write_only=True,
        source="organisatorische_eenheid",
        allow_null=True,
        required=False,
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
