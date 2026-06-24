from rest_framework import serializers

from openorganisatie.organisatie.models import Medewerker


class MedewerkerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="organisatie_api:medewerker-detail", lookup_field="uuid"
    )

    class Meta:
        model = Medewerker
        fields = [
            "url",
            "uuid",
            "external_id",
            "medewerker_id",
            "voornaam",
            "achternaam",
            "emailadres",
            "telefoonnummer",
            "geslachtsaanduiding",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
