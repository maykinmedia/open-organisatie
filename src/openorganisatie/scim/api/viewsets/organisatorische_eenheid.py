from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.organisatorische_eenheid import OrganisatorischeEenheidFilter
from ..serializers.organisatorische_eenheid import OrganisatorischeEenheidSerializer


@extend_schema(tags=["Organisatorische eenheid"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle Organisatorische eenheden  opvragen.",
        description="Alle Organisatorische eenheden opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke Organisatorische eenheid opvragen.",
        description="Een specifieke Organisatorische eenheid opvragen.",
    ),
)
class OrganisatorischeEenheidReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrganisatorischeEenheid.objects.all()
    serializer_class = OrganisatorischeEenheidSerializer
    filterset_class = OrganisatorischeEenheidFilter
    lookup_field = "name"
    lookup_url_kwarg = "naam"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
