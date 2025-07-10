from django_scim.views import UsersView

from .adapters import MedewerkerAdapter
from .models.medewerker import Medewerker


class MedewerkerUsersView(UsersView):
    @classmethod
    def scim_adapter_getter(cls):
        return MedewerkerAdapter

    @classmethod
    def model_cls_getter(cls):
        return Medewerker
