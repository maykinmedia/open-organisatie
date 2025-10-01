import uuid

from django.db import models


class OrganisatorischeEenheid(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text="Unieke resource identifier (UUID4)",
    )
    identifier = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Identificatie",
        help_text="Unieke interne identificatie van de organisatorische eenheid.",
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Naam",
        help_text="Volledige naam van de organisatorische eenheid.",
    )
    organization_type = models.CharField(
        max_length=50,
        verbose_name="Type organisatie",
        help_text="Type organisatie.",
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Verkorte naam",
        help_text="Afkorting of verkorte naam van de organisatorische eenheid.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Beschrijving",
        help_text="Optionele beschrijving van de organisatorische eenheid.",
    )
    email_address = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="E-mailadres",
        help_text="E-mailadres van de organisatorische eenheid.",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Telefoonnummer",
        help_text="Telefoonnummer van de organisatorische eenheid.",
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Einddatum",
        help_text="Optionele einddatum waarop de organisatorische eenheid wordt opgeheven of stopt te bestaan.",
    )
    branch = models.ManyToManyField(
        "scim.Vestiging",
        related_name="organisatorische_eenheden",
        blank=True,
        verbose_name="Vestigingen",
        help_text="Vestigingen waaraan de medewerker gekoppeld is.",
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="organisatorische_eenheden",
        blank=True,
        help_text="Functies binnen deze organisatorische eenheid.",
    )

    class Meta:
        verbose_name = "Organisatorische Eenheid"
        verbose_name_plural = "Organisatorische Eenheden"

    def __str__(self):
        return self.name
