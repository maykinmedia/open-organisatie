from rest_framework import serializers

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    naam = serializers.CharField(source="name")
    beschrijving = serializers.CharField(source="description", allow_blank=True)
    actief = serializers.BooleanField(source="active")

    class Meta:
        model = OrganisatorischeEenheid
        fields = [
            "id",
            "naam",
            "beschrijving",
            "actief",
        ]
