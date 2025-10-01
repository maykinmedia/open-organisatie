from rest_framework import serializers

from openorganisatie.scim.models.user import User

from .group import GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    scim_external_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    voornaam = serializers.CharField(source="first_name", read_only=True)
    achternaam = serializers.CharField(source="last_name", read_only=True)
    emailadres = serializers.EmailField(source="email", read_only=True)
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    datum_toegevoegd = serializers.DateTimeField(source="date_joined", read_only=True)
    laatst_gewijzigd = serializers.DateTimeField(source="last_modified", read_only=True)
    titel = serializers.CharField(source="job_title", allow_blank=True, required=False)
    is_active = serializers.BooleanField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "scim_external_id",
            "username",
            "voornaam",
            "achternaam",
            "emailadres",
            "telefoonnummer",
            "titel",
            "is_active",
            "groups",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
