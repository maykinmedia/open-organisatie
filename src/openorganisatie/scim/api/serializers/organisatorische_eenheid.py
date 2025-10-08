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
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "uuid"),
    )
    identificatie = serializers.CharField(
        source="identifier",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "identifier"),
    )
    naam = serializers.CharField(
        source="name",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "name"),
    )
    type_organisatie = serializers.CharField(
        source="organization_type",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "organization_type"),
    )
    verkorte_naam = serializers.CharField(
        source="short_name",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "short_name"),
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "description"),
    )
    emailadres = serializers.EmailField(
        source="email_address",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "email_address"),
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "phone_number"),
    )
    einddatum = serializers.DateField(
        source="end_date",
        allow_null=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "end_date"),
    )
    hoofd_organisatorische_eenheid = UUIDRelatedField(
        queryset=OrganisatorischeEenheid.objects.all(),
        source="parent_organisation",
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
            "type_organisatie",
            "verkorte_naam",
            "beschrijving",
            "emailadres",
            "telefoonnummer",
            "einddatum",
            "hoofd_organisatorische_eenheid",
        ]


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "uuid"),
    )
    identificatie = serializers.CharField(
        source="identifier",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "identifier"),
    )
    naam = serializers.CharField(
        source="name",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "name"),
    )
    type_organisatie = serializers.CharField(
        source="organization_type",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "organization_type"),
    )
    verkorte_naam = serializers.CharField(
        source="short_name",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "short_name"),
    )
    beschrijving = serializers.CharField(
        source="description",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "description"),
    )
    emailadres = serializers.EmailField(
        source="email_address",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "email_address"),
    )
    telefoonnummer = serializers.CharField(
        source="phone_number",
        allow_blank=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "phone_number"),
    )
    einddatum = serializers.DateField(
        source="end_date",
        allow_null=True,
        required=False,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "end_date"),
    )
    vestigingen = VestigingSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("scim.OrganisatorischeEenheid", "branches"),
    )
    vestigingen_uuid = UUIDRelatedField(
        queryset=Vestiging.objects.all(),
        write_only=True,
        source="branches",
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
        source="parent_organisation",
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
            "type_organisatie",
            "verkorte_naam",
            "beschrijving",
            "emailadres",
            "telefoonnummer",
            "einddatum",
            "vestigingen",
            "vestigingen_uuid",
            "functies",
            "functies_uuid",
            "hoofd_organisatorische_eenheid",
        ]

    def to_representation(self, instance):
        """Ensure hoofd_organisatorische_eenheid is serialized as a string UUID."""
        data = super().to_representation(instance)
        parent = instance.parent_organisation
        data["hoofd_organisatorische_eenheid"] = str(parent.uuid) if parent else None
        return data
