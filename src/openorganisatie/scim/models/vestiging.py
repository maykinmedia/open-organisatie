from django.db import models


class Vestiging(models.Model):
    naam = models.CharField(
        max_length=100, unique=True, help_text="Naam van de vestiging."
    )
    adres = models.CharField(
        max_length=255, blank=True, help_text="Adres van de vestiging (optioneel)."
    )
    medewerkers = models.ManyToManyField(
        "scim.Medewerker",
        related_name="vestigingen",
        blank=True,
        help_text="Medewerkers die aan deze vestiging gekoppeld zijn.",
    )
    organisatorische_eenheid = models.ForeignKey(
        "scim.OrganisatorischeEenheid",
        on_delete=models.CASCADE,
        related_name="vestigingen",
        help_text="De organisatorische eenheid waartoe deze vestiging behoort.",
    )
    actief = models.BooleanField(
        default=True, help_text="Geeft aan of de vestiging momenteel actief is."
    )

    def __str__(self):
        return self.naam
