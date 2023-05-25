import enum

START_MESSAGE = "Здравствуйте! Это бот фонда 'Рассправь крылья'."
HELP_MESSAGE = "Здесь выводится краткое описание возможностей бота"
ASSISTANCE_MESSAGE = "[Заглушка]Сообщение после нажатия на кнопку 'Получить помощь' (Выбор региона)"
DONATION_MESSAGE = "[Заглушка]Сообщение сопутствующее кнопке 'Сделать пожертование'"

ASSISTANCE = "assistance"  # п.с. "Помочь или получить помощь"
DONATION = "donation"  # п.с. "Перенаправление на форму с пожертвованиями"
REGION = "region"  # п.с. "Выбор региона"
BACK = "back"  # для кнопки "Назад"

ASSISTANCE_BUTTON = 'Получить помощь'
DONATION_BUTTON = 'Сделать пожертование'
BACK_BUTTON = 'Назад'


class Regions(str, enum.Enum):
    """Регионы системной работы и проектов."""

    MOSCOW_CITY = "г. Москва"
    BELGOROD_REGION = "Белгородская область"
    VLADIMIR_REGION = "Владимирская область"
    KALUGA_REGION = "Калужская область"
    SMOLENSK_REGION = "Смоленская область"
    TULA_REGION = "Тульская область"
    VOLGOGRAD_REGION = "Волгоградская область"
    KRASNOYARSK_REGION = "Красноярский край"
    LIPETSK_REGION = "Липецкая область"
    MOSCOW_REGION = "Московская область"
    PETERBURG_CITY = "г. Санкт-Петербург"
    SVERDLOVSK_REGION = "Свердловская область"
    MAGADAN_REGION = "Магаданская область"
    RYAZAN_REGION = "Рязанская область"
    SAMARA_REGION = "Самарская область"
    TVER_REGION = "Тверская область"
    UDMURTIA_REPUBLIC = "Удмуртская республика"
