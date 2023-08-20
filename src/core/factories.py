from factory import Faker
from factory.django import DjangoModelFactory

from core.models import Region


class RegionFactory(DjangoModelFactory):
    """Region model factory."""

    class Meta:
        model = Region
        django_get_or_create = ("region_name",)

    region_name = Faker("region", locale="ru_RU")
