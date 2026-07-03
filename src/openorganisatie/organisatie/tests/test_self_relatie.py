from django.core.exceptions import ValidationError
from django.test import TestCase

from openorganisatie.organisatie.models.factories.functie import FunctieFactory
from openorganisatie.organisatie.models.factories.organisatorische_eenheid import (
    OrganisatorischeEenheidFactory,
)


class SelfRelatieTests(TestCase):
    def test_prevent_self_parenting_functie(self):
        functie = FunctieFactory()
        functie.vervanger = functie
        with self.assertRaises(ValidationError) as val:
            functie.clean()
        self.assertIn(
            "vervanger",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een vervanger kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["vervanger"][0],
        )

    def test_prevent_cycle_in_parent(self):
        parent = OrganisatorischeEenheidFactory()
        child = OrganisatorischeEenheidFactory(hoofd_organisatorische_eenheid=parent)

        parent.hoofd_organisatorische_eenheid = child
        with self.assertRaises(ValidationError) as val:
            parent.clean()
        self.assertIn(
            "hoofd_organisatorische_eenheid",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan geen kind als bovenliggende eenheid hebben.",
            val.exception.message_dict["hoofd_organisatorische_eenheid"][0],
        )

    def test_prevent_self_parenting_oe(self):
        org = OrganisatorischeEenheidFactory()
        org.hoofd_organisatorische_eenheid = org
        with self.assertRaises(ValidationError) as val:
            org.clean()
        self.assertIn(
            "hoofd_organisatorische_eenheid",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een organisatorische eenheid kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["hoofd_organisatorische_eenheid"][0],
        )
