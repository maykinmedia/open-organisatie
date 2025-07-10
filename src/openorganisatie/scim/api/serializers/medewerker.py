from rest_framework import serializers

from openorganisatie.scim.models.medewerker import Medewerker


class MedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = "__all__"
