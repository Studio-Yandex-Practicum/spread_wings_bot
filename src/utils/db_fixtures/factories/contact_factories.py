from factory import Factory, Faker, LazyAttribute, SubFactory

from .service import generate_dict_factory
from .templates import (
    END_COMMON_TEMPLATE,
    MAIN_COORDINATORS_TEMPLATE,
    START_COMMON_TEMPLATE,
)


class Contacts:
    """Model to make contacts factories."""

    def __init__(self, email: str, phone_number: str, telegram: str) -> None:
        """To initialize."""
        self.email = email
        self.phone_number = phone_number
        self.telegram = telegram


class Coordinator:
    """Model to make Coordinator factories."""

    def __init__(self, name: str, region: str, contacts: Contacts) -> None:
        """To initialize."""
        self.name = name
        self.region = region
        self.contacts = contacts


class ContactsFactory(Factory):
    """Creating Contacts factory."""

    class Meta:
        """Connection to Contacts Model."""

        model = Contacts

    email = Faker("email", locale="ru_RU")
    phone_number = Faker("phone_number", locale="ru_RU")
    telegram = LazyAttribute(lambda obj: f'@{obj.email.split("@")[0]}')


class CoordinatorFactory(Factory):
    """Creating Coordinator factory."""

    class Meta:
        """Connection to Coordinator Model."""

        model = Coordinator

    name = Faker("name", locale="ru_RU")
    region = Faker("region", locale="ru_RU")
    contacts = SubFactory(ContactsFactory)


def generate_coordinators(count: int) -> str:
    """Generate html string of coordinators."""
    coordinators_data = {}
    for i in range(count):
        coordinators_data[i] = generate_dict_factory(CoordinatorFactory)()

    list_of_main_templates = []
    for coordinator in coordinators_data.values():
        contacts = coordinator.get("contacts")
        list_of_main_templates.append(
            MAIN_COORDINATORS_TEMPLATE.format(
                region=coordinator.get("region"),
                name=coordinator.get("name"),
                email=contacts.get("email"),
                phone=contacts.get("phone_number"),
                telegram=contacts.get("telegram"),
            )
        )
    result = f"{START_COMMON_TEMPLATE}{''.join(list_of_main_templates)}{END_COMMON_TEMPLATE}"
    return result


if __name__ == "__main__":
    count = int(input("Необходимое количество координаторов: "))
    coordinators = generate_coordinators(count=count)
    print(coordinators)
