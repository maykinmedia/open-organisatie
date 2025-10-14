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
        summary="Een specifiek team opvragen.",
        description="Een specifiek team opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw team aanmaken.",
        description="Voeg een nieuw team toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Team volledig bijwerken.",
        description="Werk alle gegevens van een team bij.",
    ),
    partial_update=extend_schema(
        summary="Team gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een team bij.",
    ),
    destroy=extend_schema(
        summary="Team verwijderen.",
        description="Verwijder een specifiek team.",
    ),
)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
