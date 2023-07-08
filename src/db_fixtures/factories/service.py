from functools import partial
from typing import Any, Dict

from factory.base import StubObject


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


# def factory_to_html_text(data) -> str:
#     """Create HTML template with coordinator's info."""
#     filename = "coordinator_contacts.html"
#     start_template = (
#         '<table style="border-collapse: collapse;'
#         ' width: 100.303%; height: 112px;">\n'
#         "  <tbody>\n"
#     )
#     main_template = (
#         '    <tr style="height: 16px;">\n'
#         '      <td style="width: 20%;'
#         ' height: 16px;">{region}</td>\n'
#         '      <td style="width: 20%;'
#         ' height: 16px;">{coord_name}</td>\n'
#         '      <td style="width: 20%;'
#         ' height: 16px;">{email}</td>\n'
#         '      <td style="width: 20%;'
#         ' height: 16px;">{phone}</td>\n'
#         '      <td style="width: 20%;'
#         ' height: 16px;">@{telegram}</td>\n'
#         "    </tr>\n"
#     )
#     end_template = "  </tbody>\n" "</table>\n"

#     middle = []

#     for contact in data.values():
#         coordinator = contact.get("coordinator")
#         contacts = coordinator.get("contacts")
#         middle.append(
#             main_template.format(
#                 region=contact.get("city"),
#                 coord_name=coordinator.get("name"),
#                 email=contacts.get("email"),
#                 phone=contacts.get("phone_number"),
#                 telegram=contacts.get("telegram").lower(),
#             )
#         )

#     return start_template + "".join(middle) + end_template


# def create_html_file(filename: str, data: str) -> None:
#     with open(filename, "w", encoding="utf-8") as tags:
#         tags.write(data)
