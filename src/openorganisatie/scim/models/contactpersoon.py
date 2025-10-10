import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Contactpersoon(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    medewerker = models.ForeignKey(
        "scim.Medewerker",
        on_delete=models.CASCADE,
        related_name="contactpersoon_roles",
        help_text=_("De medewerker die aan deze rol gekoppeld is."),
    )
    teams = models.ManyToManyField(
        "scim.Team",
        related_name="contactpersonen",
        blank=True,
        help_text=_("Teams waaraan de medewerker gekoppeld is."),
    )
    organisatorische_eenheden = models.ManyToManyField(
        "scim.OrganisatorischeEenheid",
        related_name="contactpersonen",
        blank=True,
        help_text=_("Organisatorische eenheden waaraan de medewerker gekoppeld is."),
    )

    class Meta:
        verbose_name = _("Contactpersoon")
        verbose_name_plural = _("Contactpersonen")

    def __str__(self):
        parts = []
        if self.teams.exists():
            parts.append("Teams: " + ", ".join([t.naam for t in self.teams.all()]))
        if self.organisatorische_eenheden.exists():
            parts.append(
                "OE: "
                + ", ".join([oe.naam for oe in self.organisatorische_eenheden.all()])
            )
        return (
            f"{self.medewerker} - " + " | ".join(parts)
            if parts
            else str(self.medewerker)
        )
