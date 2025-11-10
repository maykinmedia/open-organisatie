from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)

from ..filterset.organisatorische_eenheid import OrganisatorischeEenheidFilter
from ..serializers.organisatorische_eenheid import OrganisatorischeEenheidSerializer

logger = structlog.stdlib.get_logger(__name__)


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
class OrganisatorischeEenheidViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = OrganisatorischeEenheid.objects.all()
    serializer_class = OrganisatorischeEenheidSerializer
    filterset_class = OrganisatorischeEenheidFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        organisatie = serializer.instance
        logger.info(
            "organisatorische_eenheid_created",
            uuid=str(organisatie.uuid),
            identificatie=organisatie.identificatie,
            naam=organisatie.naam,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        organisatie = serializer.instance
        logger.info(
            "organisatorische_eenheid_updated",
            uuid=str(organisatie.uuid),
            identificatie=organisatie.identificatie,
            naam=organisatie.naam,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "organisatorische_eenheid_deleted",
            uuid=str(instance.uuid),
            identificatie=instance.identificatie,
            naam=instance.naam,
        )
