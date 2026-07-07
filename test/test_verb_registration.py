from twip.verb import VERBS, register_verb


def test_register_verb_adds_targeted_verb():
    try:
        register_verb("knock")

        assert VERBS["knock"].name == "knock"
        assert VERBS["knock"].requires_target
    finally:
        VERBS.pop("knock", None)