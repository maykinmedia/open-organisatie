import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_scim.models import AbstractSCIMGroupMixin


class Team(AbstractSCIMGroupMixin, models.Model):
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
    branch = models.ManyToManyField(
        "scim.Vestiging",
        related_name="teams",
        blank=True,
        verbose_name=_("Vestigingen"),
        help_text=_("Vestigingen waaraan de medewerker gekoppeld is."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="teams",
        blank=True,
        verbose_name=_("Functies"),
        help_text=_("Functies die binnen dit team actief zijn."),
    )

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name
