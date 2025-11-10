from django.db import models


class GenderIndicator(models.TextChoices):
    MAN = "M", "Man"
    VROUW = "V", "Vrouw"
    ANDERS = "X", "Anders"
