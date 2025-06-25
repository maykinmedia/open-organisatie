from django.urls import path
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from .viewsets.medewerker import SCIMUserViewSet

router = DefaultRouter()
router.register(r"Users", SCIMUserViewSet, basename="user")

app_name = "scim"

urlpatterns = [
    path("", TemplateView.as_view(template_name="master.html"), name="root"),
] + router.urls
