from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.identiteit.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    scim_external_id = serializers.UUIDField(
        read_only=True, help_text=get_help_text("identiteit.Group", "scim_external_id")
    )
    naam = serializers.CharField(
        source="name", help_text=get_help_text("identiteit.Group", "name")
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        help_text=get_help_text("identiteit.Group", "description"),
    )
    is_active = serializers.BooleanField(
        source="active",
        read_only=True,
        help_text=get_help_text("identiteit.Group", "active"),
    )

    class Meta:
        model = Group
        fields = ["scim_external_id", "naam", "beschrijving", "is_active"]
