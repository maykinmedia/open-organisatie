import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .relaties import FunctieTeam, OrganisatorischeEenheidFunctie


class Functie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Externe identifier voor deze functie."),
    )
    functie_omschrijving = models.CharField(
        max_length=255,
        help_text=_("Korte omschrijving of titel van de functie."),
    )
    startdatum = models.DateField(
        null=True,
        blank=True,
        help_text=_("De datum waarop de functie ingaat."),
    )
    einddatum = models.DateField(
        blank=True,
        null=True,
        help_text=_("De datum waarop de functie eindigt."),
    )
    wijzigingsdatum = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("De datum waarop de functie gewijzigd is."),
    )
    functie_type = models.ForeignKey(
        "organisatie.FunctieType",
        on_delete=models.CASCADE,
        related_name="functies",
        help_text=_("Het type functie dat hieraan gekoppeld is."),
    )
    medewerker = models.ForeignKey(
        "organisatie.Medewerker",
        on_delete=models.CASCADE,
        related_name="functies",
        blank=True,
        null=True,
        help_text=_("De medewerker die aan deze functie gekoppeld is."),
    )
    teams = models.ManyToManyField(
        "organisatie.Team",
        through=FunctieTeam,
        related_name="functies",
        blank=True,
        help_text=_("Teams van de functie."),
    )
    organisatorische_eenheid = models.ManyToManyField(
        "organisatie.OrganisatorischeEenheid",
        through=OrganisatorischeEenheidFunctie,
        related_name="functies",
        blank=True,
        help_text=_("Organisatorische eenheden van de functie."),
    )

    class Meta:
        verbose_name = _("Functie")
        verbose_name_plural = _("Functies")

    def __str__(self):
        return self.functie_omschrijving
