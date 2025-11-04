import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    naam = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Naam van het team."),
    )
    omschrijving = models.TextField(
        blank=True,
        help_text=_("Optionele omschrijving van het team."),
    )
    contactpersoon = models.ForeignKey(
        "scim.Medewerker",
        on_delete=models.SET_NULL,
        related_name="teams_als_contactpersoon",
        null=True,
        blank=True,
        help_text=_("De medewerker die contactpersoon is voor dit team."),
    )
    vestigingen = models.ManyToManyField(
        "scim.Vestiging",
        related_name="teams",
        blank=True,
        help_text=_("Vestigingen waaraan de medewerker gekoppeld is."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="teams",
        blank=True,
        verbose_name=_("Functies"),
        help_text=_("Functies die binnen dit team actief zijn."),
    )

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.naam
