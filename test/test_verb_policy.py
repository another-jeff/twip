# test/test_verb_policy.py

from twip.verb import VERBS


def test_uniform_zebra_verbs_are_registered():
    for name in [
        "about",
        "again",
        "ask",
        "break",
        "burn",
        "climb",
        "curse",
        "dig",
        "drink",
        "drop",
        "eat",
        "enter",
        "examine",
        "feel",
        "fill",
        "give",
        "go",
        "help",
        "info",
        "inventory",
        "jump",
        "listen",
        "look",
        "open",
        "pray",
        "pull",
        "put",
        "search",
        "show",
        "sing",
        "sleep",
        "smell",
        "take",
        "talk",
        "tell",
        "turn",
        "undo",
        "unlock",
        "wait",
        "wake",
        "wave",
        "wear",
    ]:
        assert name in VERBS


def test_targetless_verbs_are_explicit():
    assert not VERBS["look"].requires_target
    assert not VERBS["inventory"].requires_target
    assert not VERBS["wait"].requires_target
    assert not VERBS["again"].requires_target


def test_object_verbs_require_targets_by_default():
    assert VERBS["open"].requires_target
    assert VERBS["take"].requires_target
    assert VERBS["put"].requires_target
    assert VERBS["unlock"].requires_target