from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models.medewerker import Medewerker
from ..serializers.medewerker import MedewerkerSCIMSerializer


class SCIMUserViewSet(ModelViewSet):
    queryset = Medewerker.objects.all()
    serializer_class = MedewerkerSCIMSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
