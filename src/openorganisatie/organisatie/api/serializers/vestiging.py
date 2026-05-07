from rest_framework import serializers

from openorganisatie.organisatie.models.vestiging import Vestiging


class VestigingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vestiging
        fields = [
            "uuid",
            "external_id",
            "vestigingsnummer",
            "naam",
            "adres",
            "correspondentieadres",
            "post_adres",
            "telefoonnummer",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
