from django.db import models
from django.utils import timezone

from django_scim.models import AbstractSCIMUserMixin


class User(AbstractSCIMUserMixin, models.Model):
    username = models.CharField(
        editable=False,
        max_length=100,
        verbose_name="User principle name",
        help_text="Unieke Azure Active Directory Object ID van de medewerker.",
    )
    first_name = models.CharField(
        max_length=100, verbose_name="Voornaam", help_text="Voornaam van de medewerker."
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Achternaam",
        help_text="Achternaam van de medewerker.",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="E-mailadres",
        help_text="E-mailadres van de medewerker.",
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Functie",
        help_text="Functie van de medewerker (optioneel).",
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Telefoonnummer",
        help_text="Telefoonnummer van de medewerker (optioneel).",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Geeft aan of de medewerker momenteel actief is.",
    )
    groups = models.ManyToManyField(
        "scim.Group",
        related_name="user_set",
        blank=True,
        verbose_name="Groups",
        help_text="Groups van de user.",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Datum toegevoegd",
        help_text="Datum waarop de medewerker is toegevoegd.",
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Laatst gewijzigd",
        help_text="Datum waarop de medewerker voor het laatst is gewijzigd.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
