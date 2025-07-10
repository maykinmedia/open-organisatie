from django.urls import include, path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .schema import custom_settings
from .viewsets.medewerker import MedewerkerReadOnlyViewSet

app_name = "scim_api"

router = routers.DefaultRouter()
router.register("medewerkers", MedewerkerReadOnlyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", router.APIRootView.as_view(), name="root"),
    path(
        "schema/openapi.json",
        SpectacularJSONAPIView.as_view(
            urlconf="openorganisatie.scim.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-json-medewerkers",
    ),
    path(
        "schema/openapi.yaml",
        SpectacularYAMLAPIView.as_view(
            urlconf="openorganisatie.scim.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-yaml-medewerkers",
    ),
    path(
        "schema/",
        SpectacularRedocView.as_view(
            url_name="scim_api:schema-yaml-medewerkers",
        ),
        name="schema-redoc-medewerkers",
    ),
]
