from django.test import TestCase

from ..models.attr_mapping_config import AttribuutMappingConfig
from ..models.medewerker import Medewerker
from ..models.user import User


class KoppelMedewerkerTests(TestCase):
    def setUp(self):
        self.medewerker = Medewerker.objects.create(
            medewerker_id="123",
            emailadres="test@gmail.nl",
        )

        self.config_employee_number = AttribuutMappingConfig.objects.create(
            naam="default",
            medewerker_koppel_attribuut="employee_number",
            actief=True,
        )

        self.config_email = AttribuutMappingConfig.objects.create(
            naam="email_mapping",
            medewerker_koppel_attribuut="email",
            actief=False,
        )

        self.config_username = AttribuutMappingConfig.objects.create(
            naam="username_mapping",
            medewerker_koppel_attribuut="username",
            actief=False,
        )

    def test_koppel_medewerker_by_employee_number(self):
        user = User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.nl",
            employee_number="123",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_koppel_medewerker_by_email(self):
        self.config_employee_number.actief = False
        self.config_employee_number.save()
        self.config_email.actief = True
        self.config_email.save()

        user = User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.nl",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_koppel_medewerker_by_username(self):
        self.config_employee_number.actief = False
        self.config_employee_number.save()
        self.config_username.actief = True
        self.config_username.save()

        user = User.objects.create(
            username="test@gmail.nl",
            first_name="test",
            last_name="test",
            email="different@gmail.nl",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_no_active_config(self):
        self.config_employee_number.actief = False
        self.config_employee_number.save()

        user = User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.nl",
        )

        user.koppel_medewerker()
        self.assertIsNone(user.medewerker)

    def test_no_matching_medewerker(self):
        user = User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="nope@gmail.nl",
            employee_number="999",
        )

        user.koppel_medewerker()
        self.assertIsNone(user.medewerker)
