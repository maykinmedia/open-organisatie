from rest_framework import serializers

from openorganisatie.scim.models import Medewerker

from ..serializers.contactpersoon import ContactpersoonSerializer
from ..serializers.team import TeamSerializer
from ..serializers.vestiging import SubVestigingSerializer


class MedewerkerSerializer(serializers.ModelSerializer):
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
    teams = TeamSerializer(many=True, read_only=True)
    vestiging = SubVestigingSerializer(read_only=True)
    contactpersoon = ContactpersoonSerializer(read_only=True)
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
            "teams",
            "vestiging",
            "contactpersoon",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
