from rest_framework import serializers

from openorganisatie.scim.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    oid = serializers.UUIDField(source="scim_external_id", read_only=True)
    naam = serializers.CharField(source="name")
    beschrijving = serializers.CharField(source="description", allow_blank=True)
    actief = serializers.BooleanField(source="active")

    class Meta:
        model = Team
        fields = ["oid", "naam", "beschrijving", "actief"]
