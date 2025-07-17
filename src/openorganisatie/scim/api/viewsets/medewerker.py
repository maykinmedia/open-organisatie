from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.medewerker import MedewerkerFilter
from ..serializers.medewerker import MedewerkerSerializer
from ..serializers.team import TeamSerializer


@extend_schema(tags=["Medewerkers"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle medewerkers opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke medewerker opvragen.",
        description="Een specifieke medewerker opvragen.",
    ),
    teams=extend_schema(
        summary="Alle teams van een specifieke medewerker opvragen.",
        description="Geef een lijst terug van alle teams waar de medewerker "
        "lid van is.",
        responses={200: TeamSerializer(many=True)},
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

    @action(detail=True, methods=["get"], url_path="teams")
    def teams(self, request, *args, **kwargs):
        medewerker = self.get_object()
        teams = medewerker.scim_groups.all()
        serializer = TeamSerializer(teams, many=True, context={"request": request})
        return Response(serializer.data)
