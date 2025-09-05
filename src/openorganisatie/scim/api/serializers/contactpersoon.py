from rest_framework import serializers

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    naam = serializers.CharField(source="name")
    functie = serializers.CharField(source="function", allow_blank=True, required=False)
    emailadres = serializers.EmailField(
        source="email_address", allow_blank=True, required=False
    )
    telefoonnummer = serializers.CharField(
        source="phone_number", allow_blank=True, required=False
    )

    class Meta:
        model = Contactpersoon
        fields = ["uuid", "naam", "functie", "emailadres", "telefoonnummer"]
