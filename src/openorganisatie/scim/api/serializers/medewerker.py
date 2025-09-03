from rest_framework import serializers

from openorganisatie.scim.models import Medewerker

from ..serializers.team import TeamSerializer


class MedewerkerSerializer(serializers.ModelSerializer):
    oid = serializers.UUIDField(source="username", read_only=True)
    voornaam = serializers.CharField(source="first_name")
    achternaam = serializers.CharField(source="last_name")
    emailadres = serializers.EmailField(source="email")
    functie = serializers.CharField(
        source="job_title", allow_blank=True, required=False
    )
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    geslachtsaanduiding = serializers.BooleanField(source="gender_indicator")
    datum_uit_dienst = serializers.DateField(
        source="termination_date", required=False, allow_null=True
    )
    actief = serializers.BooleanField(source="is_active")
    teams = TeamSerializer(source="scim_groups", many=True, read_only=True)
    # TODO: add vestiging serializer
    datum_toegevoegd = serializers.DateTimeField(source="date_joined", read_only=True)
    laatst_gewijzigd = serializers.DateTimeField(source="last_modified", read_only=True)

    class Meta:
        model = Medewerker
        fields = [
            "oid",
            "voornaam",
            "achternaam",
            "emailadres",
            "functie",
            "telefoonnummer",
            "geslachtsaanduiding",
            "datum_uit_dienst",
            "actief",
            "teams",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
