import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Functie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    functie_omschrijving = models.CharField(
        max_length=255,
        help_text=_("Korte omschrijving of titel van de functie."),
    )
    begin_datum = models.DateField(
        help_text=_("De datum waarop de functie ingaat."),
    )
    eind_datum = models.DateField(
        blank=True,
        null=True,
        help_text=_("De datum waarop de functie eindigt."),
    )
    functie_type = models.ForeignKey(
        "organisatie.FunctieType",
        on_delete=models.CASCADE,
        related_name="functies",
        help_text=_("Het type functie dat hieraan gekoppeld is."),
    )

    class Meta:
        verbose_name = _("Functie")
        verbose_name_plural = _("Functies")

    def __str__(self):
        return self.functie_omschrijving
