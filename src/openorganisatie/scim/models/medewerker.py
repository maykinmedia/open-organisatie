import uuid

from django.db import models
from django.utils import timezone

from ..enums.enums import GenderIndicator


class Medewerker(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text="Unieke resource identifier (UUID4)",
    )
    medewerker_id = models.CharField(
        unique=True,
        max_length=50,
        help_text="ID van de medewerker.",
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
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Telefoonnummer",
        help_text="Telefoonnummer van de medewerker (optioneel).",
    )
    gender_indicator = models.CharField(
        choices=GenderIndicator.choices,
        max_length=10,
        blank=True,
        verbose_name="Geslachtsaanduiding",
        help_text="Geslachtsaanduiding (optioneel).",
    )
    termination_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Datum uit dienst",
        help_text="Datum waarop de medewerker uit dienst is gegaan "
        "(indien van toepassing).",
    )
    teams = models.ManyToManyField(
        "scim.Team",
        related_name="medewerker",
        blank=True,
        verbose_name="Teams",
        help_text="Teams van de medewerker.",
    )
    organisatorische_eenheden = models.ManyToManyField(
        "scim.OrganisatorischeEenheid",
        related_name="medewerkers",
        blank=True,
        verbose_name="Organisatorische Eenheden",
        help_text="Organisatorische eenheden waartoe de medewerker behoort.",
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="medewerkers",
        blank=True,
        verbose_name="Functies",
        help_text="Functies van de medewerker.",
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
        verbose_name = "Medewerker"
        verbose_name_plural = "Medewerkers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
