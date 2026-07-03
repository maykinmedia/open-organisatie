from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.organisatie.models.medewerker import Medewerker
from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)
from openorganisatie.organisatie.models.vestiging import Vestiging
from openorganisatie.utils.fields import UUIDRelatedField

from ..serializers.vestiging import VestigingSerializer


class NestedMedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = [
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
            "external_id",
            "identificatie",
            "naam",
            "soort_organisatie",
            "verkorte_naam",
            "omschrijving",
            "emailadres",
            "telefoonnummer",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
            "contactpersoon",
            "hoofd_organisatorische_eenheid",
        ]


def _creates_cycle(instance, parent):
    """
    Checks if assigning a `hoofd_organisatorische_eenheid`
    would create a cycle in the organizational hierarchy.
    Example:
    A -> B -> C

    Assigning C as the parent of A would create a cycle:
    A -> B -> C -> A
    """
    visited = set()
    current = parent

    while current:
        if current.pk == instance.pk:
            return True
        if current.pk in visited:
            break
        visited.add(current.pk)
        current = current.hoofd_organisatorische_eenheid

    return False


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    contactpersoon = NestedMedewerkerSerializer(
        read_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "contactpersoon"),
    )
    contactpersoon_uuid = UUIDRelatedField(
        queryset=Medewerker.objects.all(),
        write_only=True,
        required=False,
        help_text=get_help_text("organisatie.Team", "contactpersoon"),
        source="contactpersoon",
    )
    vestigingen = VestigingSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("organisatie.OrganisatorischeEenheid", "vestigingen"),
    )
    vestigingen_uuid = UUIDRelatedField(
        queryset=Vestiging.objects.all(),
        write_only=True,
        source="vestigingen",
        many=True,
        required=False,
        help_text=_("UUID’s van gekoppelde vestigingen."),
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
            "external_id",
            "identificatie",
            "naam",
            "soort_organisatie",
            "verkorte_naam",
            "omschrijving",
            "emailadres",
            "telefoonnummer",
            "startdatum",
            "einddatum",
            "wijzigingsdatum",
            "contactpersoon",
            "contactpersoon_uuid",
            "vestigingen",
            "vestigingen_uuid",
            "hoofd_organisatorische_eenheid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        parent = attrs.get("hoofd_organisatorische_eenheid")
        instance = self.instance

        if instance and parent and _creates_cycle(instance, parent):
            raise serializers.ValidationError(
                {
                    "hoofd_organisatorische_eenheid": _(
                        "Een organisatorische eenheid kan niet zichzelf als bovenliggende eenheid hebben."
                    )
                }
            )

        return attrs

    def to_representation(self, instance):
        """Ensure hoofd_organisatorische_eenheid is serialized as a string UUID."""
        data = super().to_representation(instance)
        parent = instance.hoofd_organisatorische_eenheid
        data["hoofd_organisatorische_eenheid"] = str(parent.uuid) if parent else None
        return data
