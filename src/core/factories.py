from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from transliterate import translit

from core.models import Region
from core.utils import to_snake_case


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region
        django_get_or_create = ("region_name",)

    region_name = Faker("region", locale="ru_RU")

    @post_generation
    def add_region_key(self, create, extracted, **kwargs):
        """Add region key field to region instance before saving."""
        translited_text = translit(self.region_name, reversed=True)
        self.region_key = to_snake_case(translited_text)
        self.save()
