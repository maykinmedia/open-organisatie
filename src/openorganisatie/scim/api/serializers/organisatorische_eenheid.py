from rest_framework import serializers

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    identificatie = serializers.CharField(source="identifier")
    naam = serializers.CharField(source="name")
    type_organisatie = serializers.CharField(source="organization_type")
    verkorte_naam = serializers.CharField(
        source="short_name", allow_blank=True, required=False
    )
    beschrijving = serializers.CharField(
        source="description", allow_blank=True, required=False
    )
    emailadres = serializers.EmailField(
        source="email_address", allow_blank=True, required=False
    )
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )
    einddatum = serializers.DateField(
        source="end_date", allow_null=True, required=False
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = [
            "uuid",
            "identificatie",
            "naam",
            "type_organisatie",
            "verkorte_naam",
            "beschrijving",
            "emailadres",
            "telefoonnummer",
            "einddatum",
        ]
