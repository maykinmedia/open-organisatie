from django.db import models

from django_scim.models import AbstractSCIMGroupMixin


class Team(AbstractSCIMGroupMixin, models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Naam van het team.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Beschrijving",
        help_text="Optionele beschrijving van het team.",
    )
    user_set = models.ManyToManyField(
        "scim.Medewerker",
        related_name="scim_groups",
        blank=True,
        verbose_name="Medewerkers",
        help_text="Medewerkers die lid zijn van dit team.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Geeft aan of het team momenteel actief is.",
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name
