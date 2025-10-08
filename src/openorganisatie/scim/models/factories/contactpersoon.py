import uuid

import factory

from openorganisatie.scim.models.contactpersoon import Contactpersoon

from .medewerker import MedewerkerFactory


class ContactpersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    medewerker = factory.SubFactory(MedewerkerFactory)

    class Meta:
        model = Contactpersoon

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.teams.set(extracted)

    @factory.post_generation
    def organisatorische_eenheden(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.organisatorische_eenheden.set(extracted)
