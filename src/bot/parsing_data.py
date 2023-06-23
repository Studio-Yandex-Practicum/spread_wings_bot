from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.extract import extract_data_from_db


class Parser:
    """Парсер."""

    def __init__(self, data: str):
        """На вход принимает html-код и скрывает его."""
        self._data = data

    async def parser_table(
        self,
    ) -> dict:
        """Парсер стандартной html-таблицы."""
        results = {"results": []}
        soup = BeautifulSoup(self._data, features="lxml")
        tbody_tag = soup.find("tbody")
        tr_tags = tbody_tag.find_all("tr")
        attributes_dict = [tr_tag.text for tr_tag in tr_tags[0]][1::2]
        for tr_tag in tr_tags[1:]:
            td_tags = tr_tag.find_all("td")
            index = 0
            result = {}
            for td_tag in td_tags:
                result[attributes_dict[index]] = td_tag.text
                index += 1
            results["results"].append(result)
        return results


async def get_coordinators(session: AsyncSession) -> dict:
    """Получеие координаторов."""
    sql_request = (
        "SELECT post_content FROM detfond_posts WHERE post_name IN"
        '("bot-kontakty-koordinatorov")'
    )
    data = await extract_data_from_db(session, sql_request)
    parser = Parser(data)
    coordinators = await parser.parser_table()
    return coordinators


async def get_regions(session: AsyncSession) -> dict:
    """Получение регионов."""
    coordinators = await get_coordinators(session)
    regions = set()
    results = dict()
    for coordinator in coordinators["results"]:
        regions.add(coordinator["Регион"])
    index = 0
    for region in list(regions):
        index += 1
        key = f"REGION_{index}"
        results[key] = region
    return results
