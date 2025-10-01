import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Vestiging(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    branchnumber = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Vestigingsnummer"),
        help_text=_("Unieke identificatiecode of nummer van de vestiging."),
    )
    branchname = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Naam"),
        help_text=_("Volledige naam van de vestiging."),
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Korte naam"),
        help_text=_("Afkorting of korte naam van de vestiging."),
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Adres"),
        help_text=_("Fysiek adres van de vestiging (optioneel)."),
    )
    correspondence_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Correspondentieadres"),
        help_text=_("Adres voor correspondentie (optioneel)."),
    )
    postal_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Post adres"),
        help_text=_("Post adres van de vestiging (optioneel)."),
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Telefoonnummer"),
        help_text=_("Telefoonnummer van de vestiging (optioneel)."),
    )
    country_code = models.CharField(
        max_length=2,
        blank=True,
        verbose_name=_("Landcode"),
        help_text=_("ISO-landcode van de vestiging (bijv. NL, BE)."),
    )

    class Meta:
        verbose_name = _("Vestiging")
        verbose_name_plural = _("Vestigingen")

    def __str__(self):
        return self.branchname
