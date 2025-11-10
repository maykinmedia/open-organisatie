from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.organisatie.models.vestiging import Vestiging

from ..serializers.vestiging import VestigingSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Vestigingen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle vestigingen opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke vestiging opvragen.",
        description="Een specifieke vestiging opvragen aan de hand van het vestigingsnummer.",
    ),
    create=extend_schema(
        summary="Nieuwe vestiging aanmaken.",
        description="Voeg een nieuwe vestiging toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Vestiging volledig bijwerken.",
        description="Werk alle gegevens van een vestiging bij.",
    ),
    partial_update=extend_schema(
        summary="Vestiging gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een vestiging bij.",
    ),
    destroy=extend_schema(
        summary="Vestiging verwijderen.",
        description="Verwijder een specifieke vestiging.",
    ),
)
class VestigingViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = Vestiging.objects.all()
    serializer_class = VestigingSerializer
    filterset_fields = {
        "naam",
        "vestigingsnummer",
        "verkorte_naam",
        "adres",
        "post_adres",
        "landcode",
    }
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        vestiging = serializer.instance
        logger.info(
            "vestiging_created",
            uuid=str(vestiging.uuid),
            vestigingsnummer=vestiging.vestigingsnummer,
            naam=vestiging.naam,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        vestiging = serializer.instance
        logger.info(
            "vestiging_updated",
            uuid=str(vestiging.uuid),
            vestigingsnummer=vestiging.vestigingsnummer,
            naam=vestiging.naam,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "vestiging_deleted",
            uuid=str(instance.uuid),
            vestigingsnummer=instance.vestigingsnummer,
            naam=instance.naam,
        )
