from django.apps import AppConfig


class OrganisatieConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "openorganisatie.organisatie"

    def ready(self):
        from . import metrics  # noqa
