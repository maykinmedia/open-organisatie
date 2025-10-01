import uuid

from django.db import models

from django_scim.models import AbstractSCIMGroupMixin


class Team(AbstractSCIMGroupMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
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
    branch = models.ManyToManyField(
        "scim.Vestiging",
        related_name="teams",
        blank=True,
        verbose_name="Vestigingen",
        help_text="Vestigingen waaraan de medewerker gekoppeld is.",
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="teams",
        blank=True,
        verbose_name="Functies",
        help_text="Functies die binnen dit team actief zijn.",
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name
