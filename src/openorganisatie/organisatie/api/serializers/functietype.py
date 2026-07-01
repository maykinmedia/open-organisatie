from rest_framework import serializers

from openorganisatie.organisatie.models.functietype import FunctieType


class FunctieTypeSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[override]
        model = FunctieType
        fields = ["uuid", "external_id", "naam", "slug"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
