from rest_framework import serializers

from openorganisatie.scim.models.vestiging import Vestiging

from .organisatorische_eenheid import OrganisatorischeEenheidSerializer


class SubVestigingSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    vestigingsnummer = serializers.CharField(source="branchnumber")
    naam = serializers.CharField(source="branchname")
    korte_naam = serializers.CharField(
        source="short_name", allow_blank=True, required=False
    )
    adres = serializers.CharField(source="address", allow_blank=True, required=False)
    correspondentieadres = serializers.CharField(
        source="correspondence_address", allow_blank=True, required=False
    )
    postadres = serializers.CharField(
        source="postal_address", allow_blank=True, required=False
    )
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    landcode = serializers.CharField(
        source="country_code", allow_blank=True, required=False
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


class VestigingSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    vestigingsnummer = serializers.CharField(source="branchnumber")
    naam = serializers.CharField(source="branchname")
    korte_naam = serializers.CharField(
        source="short_name", allow_blank=True, required=False
    )
    adres = serializers.CharField(source="address", allow_blank=True, required=False)
    correspondentieadres = serializers.CharField(
        source="correspondence_address", allow_blank=True, required=False
    )
    postadres = serializers.CharField(
        source="postal_address", allow_blank=True, required=False
    )
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    landcode = serializers.CharField(
        source="country_code", allow_blank=True, required=False
    )
    organisatorische_eenheid = OrganisatorischeEenheidSerializer(
        source="organisational_unit", read_only=True
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
            "organisatorische_eenheid",
        ]
