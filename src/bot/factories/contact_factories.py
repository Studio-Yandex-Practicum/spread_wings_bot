from factory import Factory, Faker, SubFactory
from service import factory_to_html, generate_dict_factory

NUMBER_OF_CONTACTS = 50


class Region:
    """Model to make Region factories."""

    def __init__(self, city, coordinator):
        """To initialize."""
        self.city = city
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
    """Creating Contacts factory."""

    class Meta:
        """Connection to Contacts Model."""

        model = Contacts

    email = Faker("email", locale="ru_RU")
    phone_number = Faker("phone_number", locale="ru_RU")
    telegram = Faker("first_name")


class CoordinatorFactory(Factory):
    """Creating Coordinator factory."""

    class Meta:
        """Connection to Coordinator Model."""

        model = Coordinator

    name = Faker("name", locale="ru_RU")
    contacts = SubFactory(ContactsFactory)


class RegionFactory(Factory):
    """Creating Regions factory."""

    class Meta:
        """Connection to Region Model."""

        model = Region

    city = Faker("city", locale="ru_RU")
    coordinator = SubFactory(CoordinatorFactory)


class RegionCoordinatorFactory(Factory):
    """Creating nested factories."""

    class Meta:
        """Connection to RegionCoordinator Model."""

        model = RegionCoordinator

    for i in range(1, NUMBER_OF_CONTACTS + 1):
        locals()[f"region_{i}"] = SubFactory(RegionFactory)
    del i


factory_to_dict = generate_dict_factory(RegionCoordinatorFactory)

factory_to_html(factory_to_dict())
