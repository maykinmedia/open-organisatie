from rest_framework import serializers

from openorganisatie.scim.models.team import Team

from .medewerker import MedewerkerSerializer


class TeamSerializer(serializers.ModelSerializer):
    naam = serializers.CharField(source="name")
    beschrijving = serializers.CharField(source="description", allow_blank=True)
    medewerkers = MedewerkerSerializer(source="members", many=True, read_only=True)
    actief = serializers.BooleanField(source="is_active")

    class Meta:
        model = Team
        fields = [
            "id",
            "naam",
            "beschrijving",
            "medewerkers",
            "actief",
        ]
