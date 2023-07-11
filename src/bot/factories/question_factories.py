import argparse
import os
import random
import sys

from bs4 import BeautifulSoup
from factory import Factory, Faker, SubFactory

from src.bot.constants.regions import Regions
from src.bot.factories.service import generate_dict_factory


class Question:
    """Model to make Question factories."""

    def __init__(self, question, short_description, answer, regions):
        """To initialize."""
        self.question = question
        self.short_description = short_description
        self.answer = answer
        self.regions = regions


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


class QuestionFactory(Factory):
    """Creating Question factory."""

    class Meta:
        """Connection to Question Model."""

        model = Question

    question = Faker("word", locale="ru_RU")
    short_description = Faker("text", max_nb_chars=150, locale="ru_RU")
    answer = Faker("text", max_nb_chars=1000, locale="ru_RU")
    region = Faker("address", locale="ru_RU")


class QuestionFundFactory(Factory):
    """Creating nested factories."""

    class Meta:
        """Connection to QuestionFund Model."""

        model = QuestionFund

    some_question = SubFactory(QuestionFactory)


factory_to_dict = generate_dict_factory(QuestionFactory)


def get_random_region():
    """Генерим случайные значения для региона из enum."""
    options = [
        random.choice(list(Regions)).value,
        f"{random.choice(list(Regions)).value}, {random.choice(list(Regions)).value}",
        f"{random.choice(list(Regions)).value}, "
        f"{random.choice(list(Regions)).value}, {random.choice(list(Regions)).value}",
        "",
        " ",
    ]
    city = random.choice(options)
    return city


def parse_and_recreate_record(file, question_cnt):
    """
    Отвратительная Черная Магия.

    Парсим html-контент поста, подменяем нужные поля согласно
    заданному и имеющемся кол-ву вопросов.
    """
    soup = BeautifulSoup(file, features="lxml")
    table = soup.find("table")
    trs = table.find_all("tr")
    for i in range(len(trs)):
        if i == 0:
            continue
        tds = trs[i].find_all("td")
        new_question = factory_to_dict()
        tds[0].string = new_question["question"]
        tds[1].string = new_question["short_description"]
        tds[2].string = new_question["answer"]
        tds[3].string = get_random_region()
    if len(trs) < question_cnt:
        for i in range(question_cnt - len(trs)):
            new_tr = soup.new_tag("tr", attrs={"style": "height: 16px;"})
            for j in range(4):
                new_question = factory_to_dict()
                new_question_values = list(new_question.values())
                new_td = soup.new_tag(
                    "td",
                    attrs={
                        "style": "width: 25%; height: 16px;",
                        "text": new_question_values[j],
                    },
                )
                new_tr.append(new_td)
            tbody = table.find("tbody")
            tbody.append(new_tr)
    return soup.find("table")


def generate_questions(qst_cnt):
    """Открываем сессию, получаем пост, корректируем и пишем в бд."""
    new_data = None

    with open("example.html") as file:
        post = file.read()
        new_data = str(parse_and_recreate_record(post, qst_cnt))

    with open("result.html", "w+") as new_file:
        new_file.write(new_data)


def read_arg():
    """
    Читаем аргументы командной строки.

    Ждем кол-во вопросов и их тип
    """
    parser = argparse.ArgumentParser(
        description="Утилита генерции моковых вопросов"
    )
    parser.add_argument(
        "-count",
        type=int,
        default=10,
        help="Количество вопросов для генерации",
    )
    args = parser.parse_args()
    generate_questions(args.count)


if __name__ == "__main__":
    module_path = os.path.abspath(os.getcwd() + "../../../../")
    if module_path not in sys.path:
        sys.path.append(module_path)
    read_arg()
