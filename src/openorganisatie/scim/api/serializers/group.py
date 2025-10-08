from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    scim_external_id = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Group", "scim_external_id")
    )
    naam = serializers.CharField(
        source="name", help_text=get_help_text("scim.Group", "name")
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        help_text=get_help_text("scim.Group", "description"),
    )
    is_active = serializers.BooleanField(
        source="active",
        read_only=True,
        help_text=get_help_text("scim.Group", "active"),
    )

    class Meta:
        model = Group
        fields = ["scim_external_id", "naam", "beschrijving", "is_active"]
