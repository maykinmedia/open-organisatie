from django.db import models


class FunctieType(models.Model):
    naam = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = "Functietype"
        verbose_name_plural = "Functietypes"

    def __str__(self):
        return self.naam
