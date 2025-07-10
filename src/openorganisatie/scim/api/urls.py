from django.urls import include, path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .viewsets.medewerker import MedewerkerReadOnlyViewSet

app_name = "scim_api"

router = routers.DefaultRouter()
router.register("medewerkers", MedewerkerReadOnlyViewSet)

urlpatterns = [
    path("", router.APIRootView.as_view(), name="root"),
    path("", include(router.urls)),
    # OpenAPI schema endpoints
    path(
        "schema/openapi.json",
        SpectacularJSONAPIView.as_view(urlconf="openorganisatie.scim.api.urls"),
        name="schema-json-medewerkers",
    ),
    path(
        "schema/openapi.yaml",
        SpectacularYAMLAPIView.as_view(urlconf="openorganisatie.scim.api.urls"),
        name="schema-yaml-medewerkers",
    ),
    path(
        "schema/",
        SpectacularRedocView.as_view(url_name="scim_api:schema-yaml-medewerkers"),
        name="schema-redoc-medewerkers",
    ),
]
