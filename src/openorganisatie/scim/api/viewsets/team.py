from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.team import Team
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.team import TeamFilter
from ..serializers.team import TeamSerializer


@extend_schema(tags=["Team"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle teams opvragen.",
        description="Alle teams opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke team opvragen.",
        description="Een specifieke team opvragen.",
    ),
)
class TeamReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    lookup_field = "name"
    lookup_url_kwarg = "naam"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
