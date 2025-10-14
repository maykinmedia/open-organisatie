from django.db import models


class AttribuutMappingConfig(models.Model):
    naam = models.CharField(max_length=100, unique=True)
    medewerker_koppel_attribuut = models.CharField(
        max_length=50,
        choices=[
            ("employee_number", "Employee Number (Entra)"),
            ("email", "E-mailadres"),
            ("username", "User principal name (UPN)"),
        ],
        default="employee_number",
        help_text="Bepaalt op welk attribuut de koppeling tussen User en Medewerker plaatsvindt.",
    )
    actief = models.BooleanField(default=False)

    def __str__(self):
        return self.naam
