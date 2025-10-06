from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.vestiging import Vestiging


class VestigingSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.Vestiging", "uuid")
    )
    vestigingsnummer = serializers.CharField(
        source="branchnumber", help_text=get_help_text("scim.Vestiging", "branchnumber")
    )
    naam = serializers.CharField(
        source="branchname", help_text=get_help_text("scim.Vestiging", "branchname")
    )
    korte_naam = serializers.CharField(
        source="short_name",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "short_name"),
    )
    adres = serializers.CharField(
        source="address",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "address"),
    )
    correspondentieadres = serializers.CharField(
        source="correspondence_address",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "correspondence_address"),
    )
    postadres = serializers.CharField(
        source="postal_address",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "postal_address"),
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "phone_number"),
    )
    landcode = serializers.CharField(
        source="country_code",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.Vestiging", "country_code"),
    )

    class Meta:
        model = Vestiging
        fields = [
            "uuid",
            "vestigingsnummer",
            "naam",
            "korte_naam",
            "adres",
            "correspondentieadres",
            "postadres",
            "telefoonnummer",
            "landcode",
        ]
