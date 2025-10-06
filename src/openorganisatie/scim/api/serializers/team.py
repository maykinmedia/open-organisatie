from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Team", "uuid")
    )
    naam = serializers.CharField(
        source="name", help_text=get_help_text("scim.Team", "name")
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        help_text=get_help_text("scim.Team", "description"),
    )

    class Meta:
        model = Team
        fields = ["uuid", "naam", "beschrijving"]
