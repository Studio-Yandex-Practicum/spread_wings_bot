from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def extract_data_from_db(Session: AsyncSession) -> str:
    """Извлчение html таблицы контактов координаторов из БД."""
    session = Session()
    coordinators = await session.execute(
        text(
            "SELECT post_content FROM detfond_posts WHERE post_name IN"
            '("kontakty-koordinatorov")'
        )
    )
    coordinators = coordinators.scalars().first()
    await session.close()
    return coordinators


def parser_coordinators(data: str) -> dict:
    """Парсер контактов коондинаторов из таблицы html."""
    results = {"results": []}
    soup = BeautifulSoup(data, features="lxml")
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
