from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.user import User

from .group import GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    scim_external_id = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.User", "scim_external_id")
    )
    username = serializers.CharField(
        read_only=True, help_text=get_help_text("scim.User", "username")
    )
    voornaam = serializers.CharField(
        source="first_name",
        read_only=True,
        help_text=get_help_text("scim.User", "first_name"),
    )
    achternaam = serializers.CharField(
        source="last_name",
        read_only=True,
        help_text=get_help_text("scim.User", "last_name"),
    )
    emailadres = serializers.EmailField(
        source="email", read_only=True, help_text=get_help_text("scim.User", "email")
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.User", "phone_number"),
    )
    datum_toegevoegd = serializers.DateTimeField(
        source="date_joined",
        read_only=True,
        help_text=get_help_text("scim.User", "date_joined"),
    )
    laatst_gewijzigd = serializers.DateTimeField(
        source="last_modified",
        read_only=True,
        help_text=get_help_text("scim.User", "last_modified"),
    )
    titel = serializers.CharField(
        source="job_title",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.User", "job_title"),
    )
    is_active = serializers.BooleanField(
        read_only=True, help_text=get_help_text("scim.User", "is_active")
    )
    groups = GroupSerializer(
        many=True, read_only=True, help_text=get_help_text("scim.User", "groups")
    )

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
