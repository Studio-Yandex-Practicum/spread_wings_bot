import argparse
import asyncio
import os
import random
import sys

from bs4 import BeautifulSoup
from factory import Factory, Faker, SubFactory
from sqlalchemy import Column, select
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, LONGTEXT, TEXT, VARCHAR
from sqlalchemy.orm import declarative_base

from src.bot.constants.regions import Regions
from src.bot.core.exceptions import PostNotFound
from src.bot.db.db import start_session
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

Base = declarative_base()


class PostModel(Base):
    """
    Модель постов из бд WordPress на диаклекте MYSQL.

    Все поля - чтобы не ломать посты.
    """

    __tablename__ = "detfond_posts"
    ID = Column(BIGINT, primary_key=True)
    post_author = Column(BIGINT)
    post_date = Column(DATETIME)
    post_date_gmt = Column(DATETIME)
    post_content = Column(LONGTEXT)
    post_title = Column(TEXT)
    post_excerpt = Column(TEXT)
    post_status = Column(VARCHAR(20))
    comment_status = Column(VARCHAR(20))
    ping_status = Column(VARCHAR(20))
    post_password = Column(VARCHAR(255))
    post_name = Column(VARCHAR(200))
    to_ping = Column(TEXT)
    pinged = Column(TEXT)
    post_modified = Column(DATETIME)
    post_modified_gmt = Column(DATETIME)
    post_content_filtered = Column(LONGTEXT)
    post_parent = Column(BIGINT)
    guid = Column(VARCHAR(255))
    menu_order = Column(BIGINT)
    post_type = Column(VARCHAR(20))
    post_mime_type = Column(VARCHAR(100))
    comment_count = Column(BIGINT)


QST_TYPES_TO_POST_ID = {
    "psycho": 17016,
    "social": 17018,
    "legal": 17020,
}


async def get_post(post_id, session):
    """Находим нужный нам пост."""
    post = await session.execute(
        select(PostModel).where(
            PostModel.ID == post_id,
            PostModel.post_status == "publish",
        )
    )
    return post.scalars().first()


def get_random_region():
    """Генерим случайные значения для региона из enum."""
    OPTIONS = [
        random.choice(list(Regions)).value,
        f"{random.choice(list(Regions)).value}, {random.choice(list(Regions)).value}",
        f"{random.choice(list(Regions)).value}, "
        f"{random.choice(list(Regions)).value}, {random.choice(list(Regions)).value}",
        "",
        " ",
    ]
    city = random.choice(OPTIONS)
    return city


def parse_and_recreate_record(record, question_cnt):
    """
    Отвратительная Черная Магия.

    Парсим html-контент поста, подменяем нужные поля согласно
    заданному и имеющемся кол-ву вопросов.
    """
    soup = BeautifulSoup(record.post_content, features="lxml")
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


async def insert_questions_to_db(data, record, session):
    """Записываем полученный пост в базу и защищаем закрытие сессии."""
    record.post_content = data
    session.add(record)
    await session.commit()
    await asyncio.shield(session.close())


async def generate_questions_to_db(qst_cnt, qst_type):
    """Открываем сессию, получаем пост, корректируем и пишем в бд."""
    session = await start_session()
    post = await get_post(QST_TYPES_TO_POST_ID[qst_type], session)
    if post:
        data_to_db = parse_and_recreate_record(post, qst_cnt)
        await insert_questions_to_db(data_to_db, post, session)
    else:
        raise PostNotFound(f"Пост типа {qst_type} не найден в базе")


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
    keys = list(QST_TYPES_TO_POST_ID.keys())
    parser.add_argument(
        "-type",
        choices=keys,
        default=None,
        help="Количество вопросов для генерации",
    )
    args = parser.parse_args()
    if args.type is None:
        print("Не выбран тип вопросов (-type psycho | social | legal)")
        return
    asyncio.get_event_loop().run_until_complete(
        generate_questions_to_db(args.count, args.type)
    )


if __name__ == "__main__":
    module_path = os.path.abspath(os.getcwd() + "../../../../")
    if module_path not in sys.path:
        sys.path.append(module_path)
    read_arg()
