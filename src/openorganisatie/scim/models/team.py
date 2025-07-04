from django.db import models


class Team(models.Model):
    naam = models.CharField(max_length=100, unique=True, help_text="Naam van het team.")
    beschrijving = models.TextField(
        blank=True, help_text="Optionele beschrijving van het team."
    )
    leden = models.ManyToManyField(
        "scim.Medewerker",
        related_name="teams",
        blank=True,
        help_text="Medewerkers die lid zijn van dit team.",
    )
    actief = models.BooleanField(
        default=True, help_text="Geeft aan of het team momenteel actief is."
    )

    def __str__(self):
        return self.naam
