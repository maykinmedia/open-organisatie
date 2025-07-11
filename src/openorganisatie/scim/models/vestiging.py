from django.db import models
from django.utils import timezone


class Vestiging(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Naam van de vestiging.",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adres",
        help_text="Adres van de vestiging (optioneel).",
    )
    employees = models.ManyToManyField(
        "scim.Medewerker",
        related_name="vestigingen",
        blank=True,
        verbose_name="Medewerkers",
        help_text="Medewerkers die aan deze vestiging gekoppeld zijn.",
    )
    organisational_unit = models.ForeignKey(
        "scim.OrganisatorischeEenheid",
        on_delete=models.CASCADE,
        related_name="vestigingen",
        verbose_name="Organisatorische eenheid",
        help_text="De organisatorische eenheid waartoe deze vestiging behoort.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Geeft aan of de vestiging momenteel actief is.",
    )
    date_created = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Datum toegevoegd",
        help_text="Datum waarop de vestiging is toegevoegd.",
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Laatst gewijzigd",
        help_text="Datum waarop de vestiging voor het laatst is gewijzigd.",
    )

    class Meta:
        verbose_name = "Vestiging"
        verbose_name_plural = "Vestigingen"

    def __str__(self):
        return self.name
