from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.scim.models.medewerker import Medewerker
from openorganisatie.utils.bearer import BearerTokenAuthentication

from ..filterset.medewerker import MedewerkerFilter
from ..serializers.medewerker import MedewerkerSerializer


@extend_schema(tags=["Medewerkers"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle medewerkers opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke medewerker opvragen.",
        description="Een specifieke medewerker opvragen.",
    ),
    create=extend_schema(
        summary="Nieuwe medewerker aanmaken.",
        description="Voeg een nieuwe medewerker toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Medewerker volledig bijwerken.",
        description="Werk alle gegevens van een medewerker bij.",
    ),
    partial_update=extend_schema(
        summary="Medewerker gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een medewerker bij.",
    ),
    destroy=extend_schema(
        summary="Medewerker verwijderen.",
        description="Verwijder een specifieke medewerker.",
    ),
)
class MedewerkerViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = Medewerker.objects.all()
    serializer_class = MedewerkerSerializer
    filterset_class = MedewerkerFilter
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
