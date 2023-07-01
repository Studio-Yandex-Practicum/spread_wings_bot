import sys

from factory import Factory, Faker, SubFactory
from service import generate_dict_factory


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

    city = Faker("region", locale="ru_RU")
    coordinator = SubFactory(CoordinatorFactory)


if __name__ == "__main__":
    NUMBER = int(sys.argv[1])

    class RegionCoordinatorFactory(Factory):
        """Creating nested factories."""

        class Meta:
            """Connection to RegionCoordinator Model."""

            model = RegionCoordinator

        for i in range(1, NUMBER + 1):
            locals()[f"region_{i}"] = SubFactory(RegionFactory)
        del i

    factory_to_dict = generate_dict_factory(RegionCoordinatorFactory)

    def factory_to_html(data):
        """Create HTML template with coordinator's info."""
        filename = "coordinator_contacts.html"
        start_template = (
            '<table style="border-collapse: collapse;'
            ' width: 100.303%; height: 112px;">\n'
            "  <tbody>\n"
        )
        main_template = (
            '    <tr style="height: 16px;">\n'
            '      <td style="width: 20%;'
            ' height: 16px;">{region}</td>\n'
            '      <td style="width: 20%;'
            ' height: 16px;">{coord_name}</td>\n'
            '      <td style="width: 20%;'
            ' height: 16px;">{email}</td>\n'
            '      <td style="width: 20%;'
            ' height: 16px;">{phone}</td>\n'
            '      <td style="width: 20%;'
            ' height: 16px;">@{telegram}</td>\n'
            "    </tr>\n"
        )
        end_template = "  </tbody>\n" "</table>\n"

        with open(filename, "w", encoding="utf-8") as tags:
            tags.write(start_template)
            for contact in data.values():
                coordinator = contact.get("coordinator")
                contacts = coordinator.get("contacts")
                tags.write(
                    main_template.format(
                        region=contact.get("city"),
                        coord_name=coordinator.get("name"),
                        email=contacts.get("email"),
                        phone=contacts.get("phone_number"),
                        telegram=contacts.get("telegram").lower(),
                    )
                )
            tags.write(end_template)

    factory_to_html(factory_to_dict())
