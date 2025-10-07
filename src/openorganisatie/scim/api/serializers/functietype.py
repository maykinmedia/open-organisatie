from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functietype import FunctieType


class FunctieTypeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.FunctieType", "uuid"),
    )
    naam = serializers.CharField(
        help_text=get_help_text("scim.FunctieType", "naam"),
    )
    slug = serializers.SlugField(
        help_text=get_help_text("scim.FunctieType", "slug"),
    )

    class Meta:
        model = FunctieType
        fields = ["uuid", "naam", "slug"]
