import pytest

from twip.verb import VERBS, register_verb


def test_register_verb_adds_targeted_verb():
    try:
        register_verb("knock")

        assert VERBS["knock"].name == "knock"
        assert VERBS["knock"].requires_target
    finally:
        VERBS.pop("knock", None)


def test_register_verb_rejects_duplicate_by_default():
    with pytest.raises(ValueError, match="already registered"):
        register_verb("push")


def test_register_verb_can_replace_existing_verb_when_explicit():
    original = VERBS["push"]

    try:
        register_verb("push", requires_target=False, replace=True)

        assert not VERBS["push"].requires_target
    finally:
        VERBS["push"] = original