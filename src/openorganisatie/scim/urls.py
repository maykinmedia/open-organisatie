from django.urls import path
from django.views.generic import TemplateView

from openorganisatie.scim.views import MedewerkerUsersView

app_name = "scim"

urlpatterns = [
    path("", TemplateView.as_view(template_name="master.html"), name="root"),
    path("Users", MedewerkerUsersView.as_view(), name="users"),
    path("Users/<uuid:uuid>", MedewerkerUsersView.as_view(), name="user-detail"),
]
