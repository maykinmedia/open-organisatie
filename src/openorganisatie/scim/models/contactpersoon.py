import uuid

from django.db import models


class Contactpersoon(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    medewerker = models.ForeignKey(
        "scim.Medewerker", on_delete=models.CASCADE, related_name="contactpersoon_roles"
    )
    team = models.ForeignKey(
        "scim.Team",
        on_delete=models.CASCADE,
        related_name="contactpersonen",
        null=True,
        blank=True,
    )
    organisatorische_eenheid = models.ForeignKey(
        "scim.OrganisatorischeEenheid",
        on_delete=models.CASCADE,
        related_name="contactpersonen",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Contactpersoon"
        verbose_name_plural = "Contactpersonen"
        unique_together = ("medewerker", "team", "organisatorische_eenheid")

    def __str__(self):
        if self.team:
            return f"{self.medewerker} - Team {self.team.name}"
        elif self.organisatorische_eenheid:
            return f"{self.medewerker} - OE {self.organisatorische_eenheid.name}"
        return str(self.medewerker)
