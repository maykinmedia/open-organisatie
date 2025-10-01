import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class FunctieType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor dit functietype."),
    )
    naam = models.CharField(
        max_length=50,
        help_text=_("De naam van het functietype (bijv. Manager, Medewerker)."),
        verbose_name=_("Naam"),
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text=_("Unieke, URL-vriendelijke identificatie voor dit functietype."),
        verbose_name=_("Slug"),
    )

    class Meta:
        verbose_name = _("Functietype")
        verbose_name_plural = _("Functietypes")

    def __str__(self):
        return self.naam
