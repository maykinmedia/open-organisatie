from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

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
)
class OrganisatorischeEenheidReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrganisatorischeEenheid.objects.all()
    serializer_class = OrganisatorischeEenheidSerializer
    filterset_class = OrganisatorischeEenheidFilter
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
