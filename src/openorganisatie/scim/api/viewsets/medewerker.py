from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.medewerker import MedewerkerFilter
from ..serializers.medewerker import MedewerkerSerializer


@extend_schema(tags=["Medewerkers"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle medewerkers opvragen.",
        description="Alle medewerkers opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke medewerker opvragen.",
        description="Een specifieke medewerker opvragen.",
    ),
)
class MedewerkerReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medewerker.objects.all()
    serializer_class = MedewerkerSerializer
    filterset_class = MedewerkerFilter
    lookup_field = "username"
    lookup_url_kwarg = "oid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
