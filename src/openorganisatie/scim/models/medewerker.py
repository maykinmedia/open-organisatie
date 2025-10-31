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
    )
    voornaam = models.CharField(
        max_length=100,
        help_text=_("Voornaam van de medewerker."),
    )
    achternaam = models.CharField(
        max_length=100,
        help_text=_("Achternaam van de medewerker."),
    )
    emailadres = models.EmailField(
        unique=True,
        help_text=_("E-mailadres van de medewerker."),
    )
    telefoonnummer = models.CharField(
        max_length=30,
        blank=True,
        help_text=_("Telefoonnummer van de medewerker (optioneel)."),
    )
    geslachtsaanduiding = models.CharField(
        choices=GenderIndicator.choices,
        max_length=10,
        blank=True,
        help_text=_("Geslachtsaanduiding (optioneel)."),
    )
    datum_uit_dienst = models.DateField(
        blank=True,
        null=True,
        help_text=_(
            "Datum waarop de medewerker uit dienst is gegaan (indien van toepassing)."
        ),
    )
    teams = models.ManyToManyField(
        "scim.Team",
        related_name="medewerkers",
        blank=True,
        help_text=_("Teams van de medewerker."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="medewerkers",
        blank=True,
        help_text=_("Functies van de medewerker."),
    )
    datum_toegevoegd = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text=_("Datum waarop de medewerker is toegevoegd."),
    )
    datum_aangepast = models.DateTimeField(
        auto_now=True,
        help_text=_("Datum waarop de medewerker voor het laatst is gewijzigd."),
    )

    class Meta:
        verbose_name = _("Medewerker")
        verbose_name_plural = _("Medewerkers")

    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"
