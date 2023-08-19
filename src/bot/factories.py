from factory import Faker, Iterator, LazyAttribute
from factory.django import DjangoModelFactory

from bot.models import Coordinator, FundProgram, Question
from core.models import Region


class CoordinatorFactory(DjangoModelFactory):
    """Coordinator Model Factory."""

    class Meta:
        """Metaclass for CoordinatorFactory."""

        model = Coordinator

    first_name = Faker("first_name", locale="ru_RU")
    last_name = Faker("last_name", locale="ru_RU")
    region = Iterator(Region.objects.all())
    email_address = Faker("email", locale="ru_RU")
    phone_number = Faker("phone_number", locale="ru_RU")
    telegram_account = LazyAttribute(
        lambda obj: obj.email_address.split("@")[0]
    )


class QuestionFactory(DjangoModelFactory):
    """Question Model Factory."""

    class Meta:
        """Metaclass for QuestionFactory."""

        model = Question

    question = Faker("text", max_nb_chars=200, locale="ru_RU")
    answer = Faker("text", max_nb_chars=1000, locale="ru_RU")
    short_description = Faker("text", max_nb_chars=20, locale="ru_RU")


class FundProgramFactory(DjangoModelFactory):
    """Fund Program Model Factory."""

    class Meta:
        """Metaclass for FundProgramFactory."""

        model = FundProgram

    title = Faker("word", locale="ru_RU")
    fund_text = Faker("text", max_nb_chars=500, locale="ru_RU")
    short_description = Faker("text", max_nb_chars=20, locale="ru_RU")
