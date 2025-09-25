import uuid

import factory

from openorganisatie.scim.models.contactpersoon import Contactpersoon

from .medewerker import MedewerkerFactory


class ContactpersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    medewerker = factory.SubFactory(MedewerkerFactory)
    team = None
    organisatorische_eenheid = None

    class Meta:
        model = Contactpersoon
