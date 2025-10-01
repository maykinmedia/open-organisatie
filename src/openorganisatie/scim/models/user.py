from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_scim.models import AbstractSCIMUserMixin


class User(AbstractSCIMUserMixin, models.Model):
    username = models.CharField(
        editable=False,
        max_length=100,
        verbose_name=_("User principal name"),
        help_text=_("User principal name van de medewerker."),
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("Voornaam"),
        help_text=_("Voornaam van de medewerker."),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Achternaam"),
        help_text=_("Achternaam van de medewerker."),
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("E-mailadres"),
        help_text=_("E-mailadres van de medewerker."),
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Functie"),
        help_text=_("Functie van de medewerker (optioneel)."),
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Telefoonnummer"),
        help_text=_("Telefoonnummer van de medewerker (optioneel)."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Actief"),
        help_text=_("Geeft aan of de medewerker momenteel actief is."),
    )
    groups = models.ManyToManyField(
        "scim.Group",
        related_name="user_set",
        blank=True,
        verbose_name=_("Groups"),
        help_text=_("Groups van de user."),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("Datum toegevoegd"),
        help_text=_("Datum waarop de medewerker is toegevoegd."),
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Laatst gewijzigd"),
        help_text=_("Datum waarop de medewerker voor het laatst is gewijzigd."),
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
