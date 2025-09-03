import uuid

from django.db import models


class Contactpersoon(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Naam van het team.",
    )
    function = models.TextField(
        blank=True,
        verbose_name="Beschrijving",
        help_text="Optionele beschrijving van het team.",
    )
    email_address = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="E-mailadres",
        help_text="Contact e-mailadres van de organisatorische eenheid.",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Telefoonnummer",
        help_text="Contact telefoonnummer van de organisatorische eenheid.",
    )

    class Meta:
        verbose_name = "Contactpersoon"
        verbose_name_plural = "Contactpersoon"

    def __str__(self):
        return self.name
