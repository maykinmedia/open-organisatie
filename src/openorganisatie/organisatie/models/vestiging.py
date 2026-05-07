import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Vestiging(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Externe identifier voor deze vestiging."),
    )
    naam = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Volledige naam van de vestiging."),
    )
    vestigingsnummer = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text=_("Unieke identificatiecode of nummer van de vestiging."),
    )
    kvk_nummer = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("KVK nummer van de vestiging."),
    )
    adres = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Fysiek adres van de vestiging (optioneel)."),
    )
    correspondentieadres = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Adres voor correspondentie (optioneel)."),
    )
    post_adres = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Post adres van de vestiging (optioneel)."),
    )
    telefoonnummer = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Telefoonnummer van de vestiging (optioneel)."),
    )

    class Meta:
        verbose_name = _("Vestiging")
        verbose_name_plural = _("Vestigingen")

    def __str__(self):
        return self.naam
