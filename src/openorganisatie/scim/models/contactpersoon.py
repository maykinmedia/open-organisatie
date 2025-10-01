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
        verbose_name=_("Medewerker"),
        help_text=_("De medewerker die aan deze rol gekoppeld is."),
    )
    team = models.ForeignKey(
        "scim.Team",
        on_delete=models.CASCADE,
        related_name="contactpersonen",
        null=True,
        blank=True,
        verbose_name=_("Team"),
        help_text=_("Team waaraan de medewerker gekoppeld is."),
    )
    organisatorische_eenheid = models.ForeignKey(
        "scim.OrganisatorischeEenheid",
        on_delete=models.CASCADE,
        related_name="contactpersonen",
        null=True,
        blank=True,
        verbose_name=_("Organisatorische Eenheid"),
        help_text=_("Organisatorische eenheid waaraan de medewerker gekoppeld is."),
    )

    class Meta:
        verbose_name = _("Contactpersoon")
        verbose_name_plural = _("Contactpersonen")
        unique_together = ("medewerker", "team", "organisatorische_eenheid")

    def __str__(self):
        if self.team:
            return f"{self.medewerker} - Team {self.team.name}"
        elif self.organisatorische_eenheid:
            return f"{self.medewerker} - OE {self.organisatorische_eenheid.name}"
        return str(self.medewerker)
