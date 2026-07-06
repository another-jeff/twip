from scenario import bs


def test_targetless_registered_verb_does_not_ask_what():
    s = bs().one_room()

    result = s.handle("jump")

    assert not result.ok
    assert "what" not in result.message.lower()


def test_targetless_registered_observation_verb_does_not_ask_what():
    s = bs().one_room()

    result = s.handle("listen")

    assert not result.ok
    assert "what" not in result.message.lower()


def test_target_required_registered_verb_still_asks_what():
    s = bs().one_room()

    result = s.handle("push")

    assert not result.ok
    assert "push what" in result.message.lower()