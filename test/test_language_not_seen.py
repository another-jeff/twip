from helpers import coin
from scenario import bs


def assert_not_seen(result, message: str):
    assert not result.ok
    assert result.message == message


def test_take_unresolved_target_uses_indefinite_article():
    s = bs().one_room().with_player()

    result = s.handle("take coin")

    assert_not_seen(result, "You don't see a coin here.")


def test_targeted_fallback_unresolved_target_uses_indefinite_article():
    s = bs().one_room().with_player()

    result = s.handle("open coin")

    assert_not_seen(result, "You don't see a coin here.")


def test_look_unresolved_target_uses_indefinite_article():
    s = bs().one_room().with_player()

    result = s.handle("look coin")

    assert_not_seen(result, "You don't see a coin here.")


def test_put_unresolved_destination_uses_indefinite_article():
    s = bs().one_room().with_player()
    s.put_inventory(coin)

    result = s.handle("put coin in box")

    assert_not_seen(result, "You don't see a box here.")


def test_unresolved_target_uses_an_before_vowel():
    s = bs().one_room().with_player()

    result = s.handle("take apple")

    assert_not_seen(result, "You don't see an apple here.")