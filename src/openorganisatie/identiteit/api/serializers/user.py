from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.identiteit.models.user import User

from .group import GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="identiteit_api:user-detail", lookup_field="scim_external_id"
    )
    scim_external_id = serializers.UUIDField(
        read_only=True, help_text=get_help_text("identiteit.User", "scim_external_id")
    )
    username = serializers.CharField(
        read_only=True, help_text=get_help_text("identiteit.User", "username")
    )
    emailadres = serializers.EmailField(
        source="email",
        read_only=True,
        help_text=get_help_text("identiteit.User", "email"),
    )
    datum_toegevoegd = serializers.DateTimeField(
        source="date_joined",
        read_only=True,
        help_text=get_help_text("identiteit.User", "date_joined"),
    )
    laatst_gewijzigd = serializers.DateTimeField(
        source="last_modified",
        read_only=True,
        help_text=get_help_text("identiteit.User", "last_modified"),
    )
    is_active = serializers.BooleanField(
        read_only=True, help_text=get_help_text("identiteit.User", "is_active")
    )
    groups = GroupSerializer(
        many=True, read_only=True, help_text=get_help_text("identiteit.User", "groups")
    )

    class Meta:  # type: ignore
        model = User
        fields = [
            "url",
            "scim_external_id",
            "username",
            "emailadres",
            "is_active",
            "groups",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
