import json

from factory import Factory, Faker, SubFactory

from src.bot.factories.service import generate_dict_factory


class Question:
    """Model to make Question factories."""

    def __init__(self, question, answer):
        """To initialize."""
        self.question = question
        self.answer = answer


class FundProgram:
    """Class-helper to make FundProgram factories."""

    def __init__(self, name, description):
        """To initialize."""
        self.name = name
        self.description = description


class QuestionFund:
    """Class-helper to make nested dict."""

    pass


class FundProgramFactory(Factory):
    """Creating FundPrograms factory."""

    class Meta:
        """Connection to FundProgram Model."""

        model = FundProgram

    name = Faker("word", locale="ru_RU")
    description = Faker("text", max_nb_chars=500, locale="ru_RU")


class QuestionFactory(Factory):
    """Creating Question factory."""

    class Meta:
        """Connection to Question Model."""

        model = Question

    question = Faker("word", locale="ru_RU")
    answer = Faker("text", max_nb_chars=1000, locale="ru_RU")


class QuestionFundFactory(Factory):
    """Creating nested factories."""

    class Meta:
        """Connection to QuestionFund Model."""

        model = QuestionFund

    legal_question1 = SubFactory(QuestionFactory)
    legal_question2 = SubFactory(QuestionFactory)
    social_question1 = SubFactory(QuestionFactory)
    social_question2 = SubFactory(QuestionFactory)
    psycho_question1 = SubFactory(QuestionFactory)
    psycho_question2 = SubFactory(QuestionFactory)
    fund_program1 = SubFactory(FundProgramFactory)
    fund_program2 = SubFactory(FundProgramFactory)


factory_to_dict = generate_dict_factory(QuestionFundFactory)

with open("question_data_temp.json", "w", encoding="utf-8") as f:
    json.dump(factory_to_dict(), f, indent=2, ensure_ascii=False)
