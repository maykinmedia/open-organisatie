from django.db import models


class OrganisatorischeEenheid(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Naam van de organisatorische eenheid.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Beschrijving",
        help_text="Optionele beschrijving van de organisatorische eenheid.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Geeft aan of de organisatorische eenheid actief is.",
    )

    class Meta:
        verbose_name = "Organisatorische Eenheid"
        verbose_name_plural = "Organisatorische Eenheden"

    def __str__(self):
        return self.name
