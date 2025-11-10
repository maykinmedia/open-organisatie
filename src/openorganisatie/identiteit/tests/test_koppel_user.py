from django.test import TestCase

from openorganisatie.organisatie.models.attr_mapping_config import (
    AttribuutMappingConfig,
)
from openorganisatie.organisatie.models.factories.medewerker import MedewerkerFactory

from ..constants import AttribuutChoices
from ..models.factories.user import UserFactory


class KoppelMedewerkerTests(TestCase):
    def setUp(self):
        self.medewerker = MedewerkerFactory(
            medewerker_id="123",
            emailadres="test@gmail.nl",
        )

        self.config = AttribuutMappingConfig.get_solo()
        self.config.naam = "default"
        self.config.medewerker_koppel_attribuut = AttribuutChoices.EMPLOYEE_NUMBER.value
        self.config.save()

    def test_koppel_medewerker_by_employee_number(self):
        user = UserFactory(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.nl",
            employee_number="123",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_koppel_medewerker_by_email(self):
        self.config.medewerker_koppel_attribuut = "email"
        self.config.save()

        user = UserFactory(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.nl",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_koppel_medewerker_by_username(self):
        self.config.medewerker_koppel_attribuut = "username"
        self.config.save()

        user = UserFactory(
            username="test@gmail.nl",
            first_name="test",
            last_name="test",
            email="different@gmail.nl",
        )

        user.koppel_medewerker()
        self.assertEqual(user.medewerker, self.medewerker)

    def test_no_matching_medewerker(self):
        user = UserFactory(
            username="test",
            first_name="test",
            last_name="test",
            email="nope@gmail.nl",
            employee_number="999",
        )

        user.koppel_medewerker()
        self.assertIsNone(user.medewerker)
