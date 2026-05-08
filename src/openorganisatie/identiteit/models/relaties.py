from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateRangeField
from django.contrib.postgres.fields.ranges import RangeOperators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserGroup(models.Model):
    user = models.ForeignKey("identiteit.User", on_delete=models.CASCADE)
    group = models.ForeignKey("identiteit.Group", on_delete=models.CASCADE)

    wijzigingsdatum = models.DateTimeField(auto_now=True)

    periode = DateRangeField(blank=True, null=True)

    class Meta:
        verbose_name = _("User Group")
        verbose_name_plural = _("User Groups")

        constraints = [
            ExclusionConstraint(
                name="no_overlapping_user_group_periode",
                expressions=[
                    ("user", RangeOperators.EQUAL),
                    ("group", RangeOperators.EQUAL),
                    ("periode", RangeOperators.OVERLAPS),
                ],
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.group}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.periode:
            raise ValidationError({"periode": "Periode is verplicht."})

        if not self.periode.lower:
            raise ValidationError({"periode": "Startdatum is verplicht."})

        qs = UserGroup.objects.filter(
            user_id=self.user_id,
            group_id=self.group_id,
        ).exclude(pk=self.pk)

        if qs.filter(periode__overlap=self.periode).exists():
            raise ValidationError(
                {"periode": "Deze periode overlapt met een bestaande toewijzing."}
            )
