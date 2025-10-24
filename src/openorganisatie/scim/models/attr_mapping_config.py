from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

from ..constants import AttribuutChoices


class AttribuutMappingConfig(SingletonModel):
    naam = models.CharField(max_length=100, unique=True)
    medewerker_koppel_attribuut = models.CharField(
        max_length=50,
        choices=AttribuutChoices.choices,
        default=AttribuutChoices.EMPLOYEE_NUMBER,
        help_text=_(
            "Bepaalt op welk attribuut de koppeling tussen User en Medewerker plaatsvindt."
        ),
    )

    def __str__(self):
        return self.naam
