from django.db import models
from django.utils.translation import gettext_lazy as _

ATTRIBUUT_MEDEWERKER_MAPPING = {
    "employee_number": "medewerker_id",
    "email": "emailadres",
    "username": "emailadres",
}


class AttribuutChoices(models.TextChoices):
    EMPLOYEE_NUMBER = "employee_number", _("Employee Number (Entra)")
    EMAIL = "email", _("E-mailadres")
    USERNAME = "username", _("User principal name (UPN)")
