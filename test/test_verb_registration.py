import pytest

from twip.verb import VERBS, register_verb


def test_register_verb_adds_targeted_verb(restore_verbs):
    register_verb("knock")

    assert VERBS["knock"].name == "knock"
    assert VERBS["knock"].requires_target


def test_register_verb_rejects_duplicate_by_default():
    with pytest.raises(ValueError, match="already registered"):
        register_verb("take")


def test_register_verb_can_replace_existing_verb_when_explicit(restore_verbs):
    register_verb("take", requires_target=False, replace=True)

    assert not VERBS["take"].requires_target