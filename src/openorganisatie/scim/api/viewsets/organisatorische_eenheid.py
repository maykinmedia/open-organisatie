from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.bearer import BearerTokenAuthentication

from ..filterset.organisatorische_eenheid import OrganisatorischeEenheidFilter
from ..serializers.organisatorische_eenheid import OrganisatorischeEenheidSerializer


@extend_schema(tags=["Organisatorische Eenheden"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle organisatorische eenheden opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke organisatorische eenheid opvragen.",
        description="Een specifieke organisatorische eenheid opvragen aan de hand van de identificatie.",
    ),
    create=extend_schema(
        summary="Nieuwe organisatorische eenheid aanmaken.",
        description="Voeg een nieuwe organisatorische eenheid toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Organisatorische eenheid volledig bijwerken.",
        description="Werk alle gegevens van een organisatorische eenheid bij.",
    ),
    partial_update=extend_schema(
        summary="Organisatorische eenheid gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een organisatorische eenheid bij.",
    ),
    destroy=extend_schema(
        summary="Organisatorische eenheid verwijderen.",
        description="Verwijder een specifieke organisatorische eenheid.",
    ),
)
class OrganisatorischeEenheidViewSet(viewsets.ModelViewSet):
    queryset = OrganisatorischeEenheid.objects.all()
    serializer_class = OrganisatorischeEenheidSerializer
    filterset_class = OrganisatorischeEenheidFilter
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
