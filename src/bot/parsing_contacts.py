from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.extract import extract_data_from_db


def parser_coordinators(session: AsyncSession) -> dict:
    """Парсер контактов координаторов из таблицы html."""
    sql_request = (
        "SELECT post_content FROM detfond_posts WHERE post_name IN"
        '("kontakty-koordinatorov")'
    )
    data = extract_data_from_db(session, sql_request)
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
