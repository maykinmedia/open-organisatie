import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..enums.enums import GenderIndicator


class Medewerker(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    medewerker_id = models.CharField(
        unique=True,
        max_length=50,
        help_text=_("ID van de medewerker."),
        verbose_name=_("Medewerker ID"),
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
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Telefoonnummer"),
        help_text=_("Telefoonnummer van de medewerker (optioneel)."),
    )
    gender_indicator = models.CharField(
        choices=GenderIndicator.choices,
        max_length=10,
        blank=True,
        verbose_name=_("Geslachtsaanduiding"),
        help_text=_("Geslachtsaanduiding (optioneel)."),
    )
    termination_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Datum uit dienst"),
        help_text=_(
            "Datum waarop de medewerker uit dienst is gegaan (indien van toepassing)."
        ),
    )
    teams = models.ManyToManyField(
        "scim.Team",
        related_name="medewerkers",
        blank=True,
        verbose_name=_("Teams"),
        help_text=_("Teams van de medewerker."),
    )
    organisatorische_eenheden = models.ManyToManyField(
        "scim.OrganisatorischeEenheid",
        related_name="medewerkers",
        blank=True,
        verbose_name=_("Organisatorische Eenheden"),
        help_text=_("Organisatorische eenheden waartoe de medewerker behoort."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="medewerkers",
        blank=True,
        verbose_name=_("Functies"),
        help_text=_("Functies van de medewerker."),
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
        verbose_name = _("Medewerker")
        verbose_name_plural = _("Medewerkers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
