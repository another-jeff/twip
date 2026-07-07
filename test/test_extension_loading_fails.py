import pytest

from twip.extensions import load_extension


def test_loading_same_extension_twice_fails_cleanly(restore_verbs):
    load_extension("fake_extension.knockable")

    with pytest.raises(ValueError, match="already registered"):
        load_extension("fake_extension.knockable")