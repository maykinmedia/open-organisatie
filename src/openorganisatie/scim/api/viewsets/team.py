from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.team import Team
from openorganisatie.utils.bearer import BearerTokenAuthentication

from ..filterset.team import TeamFilter
from ..serializers.team import TeamSerializer


@extend_schema(tags=["Team"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle teams opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke team opvragen.",
        description="Een specifieke medewerker opvragen.",
    ),
)
class TeamReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    lookup_field = "scim_external_id"
    lookup_url_kwarg = "oid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
