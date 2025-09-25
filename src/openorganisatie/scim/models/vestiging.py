import uuid

from django.db import models


class Vestiging(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    branchnumber = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Vestigingsnummer",
        help_text="Unieke identificatiecode of nummer van de vestiging.",
    )
    branchname = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Volledige naam van de vestiging.",
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Korte naam",
        help_text="Afkorting of korte naam van de vestiging.",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adres",
        help_text="Fysiek adres van de vestiging (optioneel).",
    )
    correspondence_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Correspondentieadres",
        help_text="Adres voor correspondentie (optioneel).",
    )
    postal_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Post adres",
        help_text="Post adres van de vestiging (optioneel).",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Telefoonnummer",
        help_text="Telefoonnummer van de vestiging (optioneel).",
    )
    country_code = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Landcode",
        help_text="ISO-landcode van de vestiging (bijv. NL, BE).",
    )

    class Meta:
        verbose_name = "Vestiging"
        verbose_name_plural = "Vestigingen"

    def __str__(self):
        return self.branchname
