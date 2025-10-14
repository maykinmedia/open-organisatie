from rest_framework import serializers

from openorganisatie.scim.models.functietype import FunctieType


class FunctieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctieType
        fields = ["uuid", "naam", "slug"]
