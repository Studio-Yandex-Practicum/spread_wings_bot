import json
from functools import partial
from random import choice
from typing import Any, Dict

from factory import Factory, Faker, SubFactory
from factory.base import StubObject

from bot.constants.regions import Regions


class Region:
    """Model to make Region factories."""

    def __init__(self, region, coordinator):
        """To initialize."""
        self.region = region
        self.coordinator = coordinator


class Coordinator:
    """Model to make Coordinator factories."""

    def __init__(self, name, contacts):
        """To initialize."""
        self.name = name
        self.contacts = contacts


class Contacts:
    """Model to make contacts factories."""

    def __init__(self, email, phone_number):
        """To initialize."""
        self.email = email
        self.phone_number = phone_number


class RegionCoordinator:
    """Class-helper to make nested dict."""

    pass


class ContactsFactory(Factory):
    """Creating Question factory."""

    class Meta:
        """Connection to Question Model."""

        model = Contacts

    email = Faker("email", locale="ru_RU")
    phone_number = Faker("phone_number", locale="ru_RU")


class CoordinatorFactory(Factory):
    """Creating Question factory."""

    class Meta:
        """Connection to Question Model."""

        model = Coordinator

    name = Faker("name", locale="ru_RU")
    contacts = SubFactory(ContactsFactory)


class RegionFactory(Factory):
    """Creating Regions factory."""

    class Meta:
        """Connection to Region Model."""

        model = Region

    region = choice(Regions)
    coordinator = SubFactory(CoordinatorFactory)


class QuestionFundFactory(Factory):
    """Creating nested factories."""

    class Meta:
        """Connection to QuestionFund Model."""

        model = RegionCoordinator

    region1 = SubFactory(RegionFactory)


def generate_dict_factory(factory):
    """To transform Factory objects into dict."""

    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)


factory_to_dict = generate_dict_factory(QuestionFundFactory)

with open("contact_data.json", "w", encoding="utf-8") as f:
    json.dump(factory_to_dict(), f, indent=2, ensure_ascii=False)
