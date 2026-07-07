from twip.extension_loader import load_extensions
from twip.verb import VERBS


class FirstExtension:
    __name__ = "first_extension"

    @staticmethod
    def register():
        VERBS["first-test"] = object()


class SecondExtension:
    __name__ = "second_extension"

    @staticmethod
    def register():
        VERBS["second-test"] = object()


def test_load_extensions_loads_each_extension():
    try:
        modules = load_extensions([FirstExtension, SecondExtension])

        assert modules == [FirstExtension, SecondExtension]
        assert "first-test" in VERBS
        assert "second-test" in VERBS
    finally:
        VERBS.pop("first-test", None)
        VERBS.pop("second-test", None)