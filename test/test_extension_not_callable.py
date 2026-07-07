import pytest

from twip.extensions import load_extension


class NoRegister:
    __name__ = "no_register"


class RegisterNotCallable:
    __name__ = "register_not_callable"
    register = "not callable"


def test_load_extension_requires_register_function():
    with pytest.raises(ValueError, match="register"):
        load_extension(NoRegister)


def test_load_extension_requires_callable_register():
    with pytest.raises(TypeError, match="not callable"):
        load_extension(RegisterNotCallable)