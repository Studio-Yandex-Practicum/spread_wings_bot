from factory import Faker
from factory.django import DjangoModelFactory

from core.models import Region


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    region_name = Faker('region', locale='ru_RU')
    region_key = Faker("text", max_nb_chars=20)
