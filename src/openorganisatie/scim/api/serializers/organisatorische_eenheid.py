from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.functie import Functie
from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.scim.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.functie import NestedFunctieSerializer
from ..serializers.vestiging import VestigingSerializer


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
            "hoofd_organisatorische_eenheid",
        ]


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
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
