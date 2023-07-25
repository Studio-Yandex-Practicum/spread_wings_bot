from functools import partial
from typing import Any, Dict

from factory.base import StubObject


def generate_dict_factory(factory):
    """To transform Factory objects into dict."""

    def stub_is_list(stub: StubObject) -> bool:
        try:
            return all(k.isdigit() for k in stub.__dict__.keys())
        except AttributeError:
            return False

    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = (
                    [
                        convert_dict_from_stub(v)
                        for v in value.__dict__.values()
                    ]
                    if stub_is_list(value)
                    else convert_dict_from_stub(value)
                )
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)
