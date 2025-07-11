from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.vestiging import Vestiging
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.vestiging import VestigingFilter
from ..serializers.vestiging import VestigingSerializer


@extend_schema(tags=["Vestiging"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle vestigingen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke vestiging opvragen.",
        description="Een specifieke vestiging opvragen.",
    ),
)
class VestigingReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vestiging.objects.all()
    serializer_class = VestigingSerializer
    filterset_class = VestigingFilter
    lookup_field = "name"
    lookup_url_kwarg = "naam"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
