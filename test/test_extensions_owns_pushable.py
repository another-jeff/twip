from twip.verb import VERBS


def test_push_is_not_registered_by_core(restore_verbs):
    assert "push" not in VERBS