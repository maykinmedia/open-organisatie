import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganisatorischeEenheid(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    identificatie = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unieke interne identificatie van de organisatorische eenheid."),
    )
    naam = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Volledige naam van de organisatorische eenheid."),
    )
    soort_organisatie = models.CharField(
        max_length=50,
        help_text=_("Soort organisatorische eenheid."),
    )
    verkorte_naam = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Afkorting of verkorte naam van de organisatorische eenheid."),
    )
    omschrijving = models.TextField(
        blank=True,
        help_text=_("Optionele omschrijving van de organisatorische eenheid."),
    )
    emailadres = models.EmailField(
        max_length=254,
        blank=True,
        help_text=_("E-mailadres van de organisatorische eenheid."),
    )
    telefoonnummer = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Telefoonnummer van de organisatorische eenheid."),
    )
    datum_opheffing = models.DateField(
        blank=True,
        null=True,
        help_text=_(
            "Optionele datum waarop de organisatorische eenheid wordt opgeheven."
        ),
    )
    contactpersoon = models.ForeignKey(
        "scim.Medewerker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organisatorische_eenheden_als_contactpersoon",
        help_text=_(
            "De medewerker die contactpersoon is voor deze organisatorische eenheid."
        ),
    )
    vestigingen = models.ManyToManyField(
        "scim.Vestiging",
        related_name="organisatorische_eenheden",
        blank=True,
        help_text=_("Vestigingen waaraan de medewerker gekoppeld is."),
    )
    functies = models.ManyToManyField(
        "scim.Functie",
        related_name="organisatorische_eenheden",
        blank=True,
        verbose_name=_("Functies"),
        help_text=_("Functies binnen deze organisatorische eenheid."),
    )
    hoofd_organisatorische_eenheid = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sub_organisatorische_eenheden",
        help_text=_("Optionele bovenliggende organisatorische eenheid."),
    )

    class Meta:
        verbose_name = _("Organisatorische Eenheid")
        verbose_name_plural = _("Organisatorische Eenheden")

    def __str__(self):
        return self.naam

    def clean(self):
        if (
            self.hoofd_organisatorische_eenheid
            and self.hoofd_organisatorische_eenheid == self
        ):
            raise ValidationError(
                {
                    "hoofd_organisatorische_eenheid": _(
                        "Een organisatorische eenheid kan niet naar zichzelf verwijzen."
                    )
                }
            )
        parent = self.hoofd_organisatorische_eenheid
        while parent:
            if parent == self:
                raise ValidationError(
                    {
                        "hoofd_organisatorische_eenheid": _(
                            "Een organisatorische eenheid kan geen kind als bovenliggende eenheid hebben."
                        )
                    }
                )
            parent = parent.hoofd_organisatorische_eenheid
