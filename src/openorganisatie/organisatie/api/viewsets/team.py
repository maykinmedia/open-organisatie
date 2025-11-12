from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.organisatie.models.team import Team

from ..filterset.team import TeamFilter
from ..serializers.team import TeamSerializer

logger = structlog.stdlib.get_logger(__name__)


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
class TeamViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        team = serializer.instance
        logger.info(
            "team_created",
            uuid=str(team.uuid),
            naam=team.naam,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        team = serializer.instance
        logger.info(
            "team_updated",
            uuid=str(team.uuid),
            naam=team.naam,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "team_deleted",
            uuid=str(instance.uuid),
            naam=instance.naam,
        )
