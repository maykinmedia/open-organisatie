from rest_framework import serializers

from openorganisatie.organisatie.models.functietype import FunctieType


class FunctieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctieType
        fields = ["uuid", "naam", "slug"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
