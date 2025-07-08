from django.db import models
from django.utils import timezone

from django_scim.models import AbstractSCIMCommonAttributesMixin


class Medewerker(AbstractSCIMCommonAttributesMixin, models.Model):
    azure_oid = models.UUIDField(
        unique=True,
        editable=False,
        help_text="Unieke Azure Active Directory Object ID van de medewerker.",
    )
    voornaam = models.CharField(max_length=100, help_text="Voornaam van de medewerker.")
    achternaam = models.CharField(
        max_length=100, help_text="Achternaam van de medewerker."
    )
    emailadres = models.EmailField(
        unique=True, help_text="Uniek e-mailadres van de medewerker."
    )
    functie = models.CharField(
        max_length=100,
        blank=True,
        help_text="Functie of functiebenaming van de medewerker (optioneel).",
    )
    telefoonnummer = models.CharField(
        max_length=30,
        blank=True,
        help_text="Telefoonnummer van de medewerker (optioneel).",
    )
    geslachtsaanduiding = models.BooleanField(
        default=True,
        help_text="Geslachtsaanduiding: waar of niet waar.???(staat zo in datamodel)",
    )
    datum_uit_dienst = models.DateField(
        blank=True,
        null=True,
        help_text="Datum waarop de medewerker uit dienst is gegaan"
        " (indien van toepassing).",
    )
    actief = models.BooleanField(
        default=True, help_text="Geeft aan of de medewerker momenteel actief is."
    )
    datum_toegevoegd = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Datum waarop de medewerker is toegevoegd.",
    )
    laatst_gewijzigd = models.DateTimeField(
        auto_now=True,
        help_text="Datum waarop de medewerker voor het laatst is gewijzigd.",
    )

    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"

    @property
    def username(self):
        return self.azure_oid

    @username.setter
    def username(self, value):
        self.azure_oid = value

    @property
    def first_name(self):
        return self.voornaam

    @first_name.setter
    def first_name(self, value):
        self.voornaam = value

    @property
    def last_name(self):
        return self.achternaam

    @last_name.setter
    def last_name(self, value):
        self.achternaam = value

    @property
    def email(self):
        return self.emailadres

    @email.setter
    def email(self, value):
        self.emailadres = value

    @property
    def is_active(self):
        return self.actief

    @is_active.setter
    def is_active(self, value):
        self.actief = value

    @property
    def date_joined(self):
        return self.datum_toegevoegd

    @date_joined.setter
    def date_joined(self, value):
        self.datum_toegevoegd = value

    @property
    def last_modified(self):
        return self.laatst_gewijzigd

    @last_modified.setter
    def last_modified(self, value):
        self.laatst_gewijzigd = value
