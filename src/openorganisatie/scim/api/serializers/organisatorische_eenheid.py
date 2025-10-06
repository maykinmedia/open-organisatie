from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(
        read_only=True, help_text=get_help_text("scim.OrganisatorischeEenheid", "uuid")
    )
    identificatie = serializers.CharField(
        source="identifier",
        help_text=get_help_text("scim.OrganisatorischeEenheid", "identifier"),
    )
    naam = serializers.CharField(
        source="name", help_text=get_help_text("scim.OrganisatorischeEenheid", "name")
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
    hoofd_organisatorische_eenheid = serializers.UUIDField(
        source="parent_organisation.uuid",
        read_only=True,
        required=False,
        help_text=_("UUID van de bovenliggende organisatorsiche eenheden."),
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
