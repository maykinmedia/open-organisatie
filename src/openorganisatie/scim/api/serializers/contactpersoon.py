from rest_framework import serializers

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    medewerker = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    organisatorische_eenheid = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Contactpersoon
        fields = ["uuid", "medewerker", "team", "organisatorische_eenheid"]
