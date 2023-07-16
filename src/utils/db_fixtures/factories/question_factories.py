from factory import Factory, Faker

from .service import generate_dict_factory
from .templates import (
    END_COMMON_TEMPLATE,
    MAIN_QUESTONS_TEMPLATE,
    START_COMMON_TEMPLATE,
)


class Question:
    """Model to make Question factories."""

    def __init__(self, question, short_description, answer, regions):
        """To initialize."""
        self.question = question
        self.short_description = short_description
        self.answer = answer
        self.regions = regions


class QuestionFactory(Factory):
    """Creating Question factory."""

    class Meta:
        """Connection to Question Model."""

        model = Question

    question = Faker("text", max_nb_chars=150, locale="ru_RU")
    short_description = Faker("text", max_nb_chars=50, locale="ru_RU")
    answer = Faker("text", max_nb_chars=1000, locale="ru_RU")
    # TODO сделать несколько регионов в строке через запятую
    regions = Faker("region", locale="ru_RU")


def generate_questions(count: int) -> str:
    """Generate html string of coordinators."""
    questions_data = {}
    for i in range(count):
        questions_data[i] = generate_dict_factory(QuestionFactory)()

    list_of_main_templates = []
    for question in questions_data.values():
        list_of_main_templates.append(
            MAIN_QUESTONS_TEMPLATE.format(
                question=question.get("question"),
                short_description=question.get("short_description"),
                answer=question.get("answer"),
                regions=question.get("regions"),
            )
        )
    result = f"{START_COMMON_TEMPLATE}{''.join(list_of_main_templates)}{END_COMMON_TEMPLATE}"
    return result


if __name__ == "__main__":
    count = int(input("Необходимое количество вопросов: "))
    questions = generate_questions(count=count)
    print(questions)
