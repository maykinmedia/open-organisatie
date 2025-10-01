import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_scim.models import AbstractSCIMGroupMixin


class Group(AbstractSCIMGroupMixin, models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Naam"),
        help_text=_("Naam van het team."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Beschrijving"),
        help_text=_("Optionele beschrijving van het team."),
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("Actief"),
        help_text=_("Geeft aan of het team momenteel actief is."),
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name
