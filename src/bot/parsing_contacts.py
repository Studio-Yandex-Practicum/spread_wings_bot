from pprint import pprint

import requests_cache
from bs4 import BeautifulSoup
from constants.urls import CONTACTS_URL


def parser() -> None:
    """Парсер контактов кураторов."""
    session = requests_cache.CachedSession()
    response = session.get(CONTACTS_URL)
    response.encoding = "utf-8"
    results = []
    soup = BeautifulSoup(response.text, features="lxml")
    body_tag = soup.body
    div_container_tag = body_tag.find("div", attrs={"class": "container"})
    div_content_tag = div_container_tag.find(
        "div", attrs={"class": "content-wrap"}
    )
    art_hide_tag = div_content_tag.find("article", attrs={"class": "autohide"})
    div_art_tag = art_hide_tag.find("div", attrs={"class": "article-text"})
    tbody_tag = div_art_tag.find("tbody")
    tr_tags = tbody_tag.find_all("tr")
    attributes_dict = [tr_tag.text for tr_tag in tr_tags[0]][1::2]
    for tr_tag in tr_tags[1:]:
        td_tags = tr_tag.find_all("td")
        index = 0
        result = {}
        for td_tag in td_tags:
            result[attributes_dict[index]] = td_tag.text
            index += 1
        results.append(result)
    pprint(results)
