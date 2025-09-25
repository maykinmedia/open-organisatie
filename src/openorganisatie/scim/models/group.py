import uuid

from django.db import models

from django_scim.models import AbstractSCIMGroupMixin


class Group(AbstractSCIMGroupMixin, models.Model):
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
    active = models.BooleanField(
        default=True,
        verbose_name="Actief",
        help_text="Geeft aan of het team momenteel actief is.",
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name
