from rest_framework import serializers

from openorganisatie.scim.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    naam = serializers.CharField(source="name")
    beschrijving = serializers.CharField(source="description", allow_blank=True)

    class Meta:
        model = Team
        fields = ["uuid", "naam", "beschrijving"]
