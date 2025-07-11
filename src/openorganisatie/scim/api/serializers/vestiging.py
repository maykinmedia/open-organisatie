from rest_framework import serializers

from openorganisatie.scim.models.vestiging import Vestiging

from .medewerker import MedewerkerSerializer
from .organisatorische_eenheid import OrganisatorischeEenheidSerializer


class VestigingSerializer(serializers.ModelSerializer):
    naam = serializers.CharField(source="name")
    adres = serializers.CharField(source="address", allow_blank=True)
    medewerkers = MedewerkerSerializer(source="employees", many=True, read_only=True)
    organisatorische_eenheid = OrganisatorischeEenheidSerializer(
        source="organisational_unit", read_only=True
    )
    actief = serializers.BooleanField(source="active")
    datum_toegevoegd = serializers.DateTimeField(source="date_created", read_only=True)
    laatst_gewijzigd = serializers.DateTimeField(source="last_modified", read_only=True)

    class Meta:
        model = Vestiging
        fields = [
            "id",
            "naam",
            "adres",
            "medewerkers",
            "organisatorische_eenheid",
            "actief",
            "datum_toegevoegd",
            "laatst_gewijzigd",
        ]
