from rest_framework import serializers

from ..models.medewerker import Medewerker


class MedewerkerSCIMSerializer(serializers.ModelSerializer):
    medewerker_id = serializers.CharField(required=False, allow_blank=True)
    userName = serializers.EmailField(source="emailadres")
    name = serializers.DictField(child=serializers.CharField(), required=False)
    active = serializers.BooleanField(source="actief", default=True)
    phoneNumbers = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = Medewerker
        fields = ["id", "medewerker_id", "userName", "name", "active", "phoneNumbers"]
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)

        name = data.get("name", {})
        internal["voornaam"] = name.get("givenName", "")
        internal["achternaam"] = name.get("familyName", "")

        phone_numbers = data.get("phoneNumbers", [])
        internal["telefoonnummer"] = (
            phone_numbers[0].get("value", "") if phone_numbers else ""
        )

        # Remove non model fields
        internal.pop("name", None)
        internal.pop("phoneNumbers", None)

        return internal

    def to_representation(self, instance):
        return {
            "id": str(instance.pk),
            "medewerker_id": instance.medewerker_id,
            "userName": instance.emailadres,
            "name": {
                "givenName": instance.voornaam,
                "familyName": instance.achternaam,
            },
            "active": instance.actief,
            "phoneNumbers": [{"value": instance.telefoonnummer, "type": "work"}]
            if instance.telefoonnummer
            else [],
        }
