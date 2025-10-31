from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.functie import NestedFunctieSerializer
from ..serializers.vestiging import VestigingSerializer


class NestedMedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = [
            "uuid",
            "medewerker_id",
            "voornaam",
            "achternaam",
            "emailadres",
            "telefoonnummer",
            "geslachtsaanduiding",
            "datum_uit_dienst",
            "datum_toegevoegd",
            "datum_aangepast",
        ]


class NestedOrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    hoofd_organisatorische_eenheid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        required=False,
        allow_null=True,
        help_text=_("UUID van de bovenliggende organisatorische eenheid (optioneel)."),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = [
            "uuid",
            "identificatie",
            "naam",
            "soort_organisatie",
            "verkorte_naam",
            "omschrijving",
            "emailadres",
            "telefoonnummer",
            "datum_opheffing",
            "contactpersoon",
            "hoofd_organisatorische_eenheid",
        ]


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    contactpersoon = NestedMedewerkerSerializer(
        read_only=True,
        required=False,
        help_text=get_help_text("scim.Team", "vestigingen"),
    )
    vestigingen = VestigingSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "vestigingen"),
    )
    vestigingen_uuid = UUIDRelatedField(
        queryset=Vestiging.objects.all(),
        write_only=True,
        source="vestigingen",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde vestigingen."),
    )
    functies = NestedFunctieSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "functies"),
    )
    functies_uuid = UUIDRelatedField(
        queryset=Functie.objects.all(),
        write_only=True,
        source="functies",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde functies."),
    )
    hoofd_organisatorische_eenheid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        required=False,
        allow_null=True,
        help_text=_("UUID van de bovenliggende organisatorische eenheid (optioneel)."),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = [
            "uuid",
            "identificatie",
            "naam",
            "soort_organisatie",
            "verkorte_naam",
            "omschrijving",
            "emailadres",
            "telefoonnummer",
            "datum_opheffing",
            "contactpersoon",
            "vestigingen",
            "vestigingen_uuid",
            "functies",
            "functies_uuid",
            "hoofd_organisatorische_eenheid",
        ]

    def to_representation(self, instance):
        """Ensure hoofd_organisatorische_eenheid is serialized as a string UUID."""
        data = super().to_representation(instance)
        parent = instance.hoofd_organisatorische_eenheid
        data["hoofd_organisatorische_eenheid"] = str(parent.uuid) if parent else None
        return data
