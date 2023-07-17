from factory import Factory, Faker, SubFactory


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


class FundProgramNestedFactory(Factory):
    """Creating nested factories."""

    class Meta:
        """Connection to FundProgram Model."""

        model = QuestionFund

    fund_program1 = SubFactory(FundProgramFactory)
    fund_program2 = SubFactory(FundProgramFactory)


# class QuestionFundFactory(Factory):
#     """Creating nested factories."""

#     class Meta:
#         """Connection to QuestionFund Model."""

#         model = QuestionFund

#     some_question = SubFactory(QuestionFactory)
