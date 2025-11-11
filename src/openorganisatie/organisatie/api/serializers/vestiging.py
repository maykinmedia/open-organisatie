from rest_framework import serializers

from openorganisatie.organisatie.models.vestiging import Vestiging


class VestigingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vestiging
        fields = [
            "uuid",
            "vestigingsnummer",
            "naam",
            "verkorte_naam",
            "adres",
            "correspondentieadres",
            "post_adres",
            "telefoonnummer",
            "landcode",
        ]
