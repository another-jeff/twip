# test/test_extensions.py

from types import ModuleType

import pytest

from twip.extensions import load_extension, load_extensions
from twip.verb import VERBS


def test_load_extension_accepts_import_path(restore_verbs):
    assert "push" not in VERBS

    module = load_extension("twip_ext.pushable")

    assert module.__name__ == "twip_ext.pushable"
    assert "push" in VERBS


def test_load_extension_accepts_module_object(restore_verbs):
    from twip_ext import pushable

    assert "push" not in VERBS

    module = load_extension(pushable)

    assert module is pushable
    assert "push" in VERBS


def test_load_extension_requires_register_function():
    module = ModuleType("fake_extension_without_register")

    with pytest.raises(ValueError, match="register"):
        load_extension(module)


def test_load_extension_rejects_non_callable_register():
    module = ModuleType("fake_extension_with_bad_register")
    module.register = "not callable"

    with pytest.raises(TypeError, match="not callable"):
        load_extension(module)


def test_load_extensions_loads_each_extension(restore_verbs):
    modules = load_extensions(("twip_ext.pushable",))

    assert [module.__name__ for module in modules] == ["twip_ext.pushable"]
    assert "push" in VERBS


def test_loading_same_extension_twice_is_not_idempotent(restore_verbs):
    load_extension("twip_ext.pushable")

    with pytest.raises(ValueError, match="already registered"):
        load_extension("twip_ext.pushable")