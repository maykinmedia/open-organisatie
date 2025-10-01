import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganisatorischeEenheid(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    identifier = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Identificatie"),
        help_text=_("Unieke interne identificatie van de organisatorische eenheid."),
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Naam"),
        help_text=_("Volledige naam van de organisatorische eenheid."),
    )
    organization_type = models.CharField(
        max_length=50,
        verbose_name=_("Type organisatie"),
        help_text=_("Type organisatie."),
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Verkorte naam"),
        help_text=_("Afkorting of verkorte naam van de organisatorische eenheid."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Beschrijving"),
        help_text=_("Optionele beschrijving van de organisatorische eenheid."),
    )
    email_address = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name=_("E-mailadres"),
        help_text=_("E-mailadres van de organisatorische eenheid."),
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Telefoonnummer"),
        help_text=_("Telefoonnummer van de organisatorische eenheid."),
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Einddatum"),
        help_text=_(
            "Optionele einddatum waarop de organisatorische eenheid wordt opgeheven of stopt te bestaan."
        ),
    )
    branch = models.ManyToManyField(
        "scim.Vestiging",
        related_name="organisatorische_eenheden",
        blank=True,
        verbose_name=_("Vestigingen"),
        help_text=_("Vestigingen waaraan de medewerker gekoppeld is."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="organisatorische_eenheden",
        blank=True,
        verbose_name=_("Functies"),
        help_text=_("Functies binnen deze organisatorische eenheid."),
    )

    class Meta:
        verbose_name = _("Organisatorische Eenheid")
        verbose_name_plural = _("Organisatorische Eenheden")

    def __str__(self):
        return self.name
