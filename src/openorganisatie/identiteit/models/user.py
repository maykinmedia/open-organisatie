from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import structlog
from django_scim.models import AbstractSCIMUserMixin

from openorganisatie.organisatie.models.attr_mapping_config import (
    AttribuutMappingConfig,
)
from openorganisatie.organisatie.models.medewerker import Medewerker

from ..constants import ATTRIBUUT_MEDEWERKER_MAPPING

logger = structlog.get_logger(__name__)


class User(AbstractSCIMUserMixin, models.Model):
    username = models.CharField(
        editable=False,
        max_length=100,
        verbose_name=_("User principal name"),
        help_text=_("User principal name van de medewerker."),
    )
    employee_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("EmployeeNumber uit Entra / SCIM."),
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("Voornaam"),
        help_text=_("Voornaam van de medewerker."),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Achternaam"),
        help_text=_("Achternaam van de medewerker."),
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("E-mailadres"),
        help_text=_("E-mailadres van de medewerker."),
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Functie"),
        help_text=_("Functie van de medewerker (optioneel)."),
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Telefoonnummer"),
        help_text=_("Telefoonnummer van de medewerker (optioneel)."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Actief"),
        help_text=_("Geeft aan of de medewerker momenteel actief is."),
    )
    groups = models.ManyToManyField(
        "identiteit.Group",
        related_name="user_set",
        blank=True,
        verbose_name=_("Groups"),
        help_text=_("Groups van de user."),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("Datum toegevoegd"),
        help_text=_("Datum waarop de medewerker is toegevoegd."),
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Laatst gewijzigd"),
        help_text=_("Datum waarop de medewerker voor het laatst is gewijzigd."),
    )
    medewerker = models.ForeignKey(
        "organisatie.Medewerker",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        help_text=_(
            "De gekoppelde medewerker (optioneel, wordt automatisch gekoppeld)."
        ),
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def koppel_medewerker(self):
        """Link User to Medewerker based on configuration."""
        config = AttribuutMappingConfig.get_solo()

        attribuut = config.medewerker_koppel_attribuut
        value = getattr(self, attribuut, None)
        if not value:
            logger.debug("geen_waarden_gevonden", attribuut=attribuut)
            return

        medewerker_field = ATTRIBUUT_MEDEWERKER_MAPPING.get(attribuut)
        if not medewerker_field:
            logger.warning("ongeldige_mapping_keuze", attribuut=attribuut)
            return

        medewerkers = Medewerker.objects.filter(**{medewerker_field: value})

        if not medewerkers.exists():
            logger.info(
                "geen_medewerker_gevonden",
                username=self.username,
                attribuut=attribuut,
                waarde=value,
            )
        elif medewerkers.count() > 1:
            logger.info(
                "meerdere_medewerkers_gevonden",
                username=self.username,
                attribuut=attribuut,
                waarde=value,
            )
        else:
            medewerker = medewerkers.first()
            if self.medewerker != medewerker:
                self.medewerker = medewerker
                self.save(update_fields=["medewerker"])
                logger.info(
                    "medewerker_koppeling_gemaakt",
                    username=self.username,
                    medewerker_id=medewerker.medewerker_id,
                    mapping_choice=attribuut,
                )
