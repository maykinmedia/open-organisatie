import uuid

from django.db import models


class FunctieType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text="Unieke resource identifier (UUID4) voor dit functietype.",
    )
    naam = models.CharField(
        max_length=50,
        help_text="De naam van het functietype (bijv. Manager, Medewerker).",
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="Unieke, URL-vriendelijke identificatie voor dit functietype.",
    )

    class Meta:
        verbose_name = "Functietype"
        verbose_name_plural = "Functietypes"

    def __str__(self):
        return self.naam
