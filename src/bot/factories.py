from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from bot.models import Coordinator, FundProgram, Question
from core.factories import RegionFactory


class CoordinatorFactory(DjangoModelFactory):
    class Meta:
        model = Coordinator

    first_name = Faker("first_name", locale="ru_RU")
    last_name = Faker("last_name", locale="ru_RU")
    region = SubFactory(RegionFactory)
    email_address = Faker("email", locale="ru_RU")
    phone_number = Faker("phone_number", locale="ru_RU")
    telegram_account = LazyAttribute(
        lambda obj: f'@{obj.email_address.split("@")[0]}'
    )


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    question = Faker("text", max_nb_chars=200, locale="ru_RU")
    answer = Faker("text", max_nb_chars=1000, locale="ru_RU")
    short_description = Faker("text", max_nb_chars=20, locale="ru_RU")


class FundProgramFactory(DjangoModelFactory):
    class Meta:
        model = FundProgram

    title = Faker("word", locale="ru_RU")
    description = Faker("text", max_nb_chars=500, locale="ru_RU")
