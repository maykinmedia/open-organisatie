from django.urls import include, path

from drf_spectacular.views import (
    SpectacularRedocView,
)
from vng_api_common import routers

from ...utils.views import SpectacularJSONAPIView, SpectacularYAMLAPIView
from .schema import custom_settings
from .viewsets.functie import FunctieViewSet
from .viewsets.functietype import FunctieTypeViewSet
from .viewsets.medewerker import MedewerkerViewSet
from .viewsets.organisatorische_eenheid import OrganisatorischeEenheidViewSet
from .viewsets.team import TeamViewSet
from .viewsets.vestiging import VestigingViewSet

app_name = "organisatie_api"

router = routers.DefaultRouter()
router.register("medewerkers", MedewerkerViewSet)
router.register("vestiging", VestigingViewSet)
router.register("organisatorische-eenheid", OrganisatorischeEenheidViewSet)
router.register("teams", TeamViewSet)
router.register("functie", FunctieViewSet)
router.register("functietype", FunctieTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", router.APIRootView.as_view(), name="root"),
    path(
        "openapi.json",
        SpectacularJSONAPIView.as_view(
            urlconf="openorganisatie.organisatie.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-json-organisatie",
    ),
    path(
        "openapi.yaml",
        SpectacularYAMLAPIView.as_view(
            urlconf="openorganisatie.organisatie.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-yaml-organisatie",
    ),
    path(
        "schema/",
        SpectacularRedocView.as_view(
            url_name="organisatie_api:schema-yaml-organisatie",
        ),
        name="schema-redoc-organisatie",
    ),
]
