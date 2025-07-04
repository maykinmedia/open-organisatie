from django.db import models


class OrganisatorischeEenheid(models.Model):
    naam = models.CharField(
        max_length=100, unique=True, help_text="Naam van de organisatorische eenheid."
    )
    beschrijving = models.TextField(
        blank=True, help_text="Optionele beschrijving van de organisatorische eenheid."
    )
    actief = models.BooleanField(
        default=True, help_text="Geeft aan of de organisatorische eenheid actief is."
    )

    def __str__(self):
        return self.naam
